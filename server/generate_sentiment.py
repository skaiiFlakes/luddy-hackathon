import os
import ast

from scraping import parse_csv as pc
from scraping import social_scraping as ss
from sentiment import social_sentiment_analysis as ssa
from get_competitors import get_competitors as gc
from scraping import news_scraping as ns
from scraping import financial_news_scraping as fns
from sentiment import news_sentiment_analysis as nsa

from dotenv import load_dotenv
load_dotenv()

def generate_config(subreddits: list[str] = [],
                    search_terms: list[str] = [],
                    posts_per_search: int = 10,
                    comments_per_post: int = 5,
                    sort_method: str = 'top',
                    time_filter: str = 'month',
                    config_file: str = './reddit_config.txt',
                    overwrite: bool = False
                    ) -> None:
    """
        Generate a configuration file for Reddit API scraping.

        Parameters:
        -----------
        search_terms : list or str
            list of search terms or comma-separated string
        subreddits : list or str
            list of subreddits or comma-separated string
        posts_per_search : int
            Number of posts to retrieve per search term
        comments_per_post : int
            Number of comments to retrieve per post
        sort_method : str
            Sort method for posts ('hot', 'new', 'top', 'relevant')
        time_filter : str
            Time filter for posts ('hour', 'day', 'week', 'month', 'year', 'all')
    """

    # Convert string inputs to lists if necessary
    if isinstance(search_terms, str):
        search_terms = [term.strip() for term in search_terms.split(',')]
    if isinstance(subreddits, str):
        subreddits = [sub.strip() for sub in subreddits.split(',')]

    # Validate inputs
    valid_sort_methods = ['hot', 'new', 'top', 'relevant']
    valid_time_filters = ['hour', 'day', 'week', 'month', 'year', 'all']

    if sort_method not in valid_sort_methods:
        raise ValueError(f"Sort method must be one of {valid_sort_methods}")
    if time_filter not in valid_time_filters:
        raise ValueError(f"Time filter must be one of {valid_time_filters}")

    # Create configuration content
    config_content = [
        "# Search Parameters",
        f"search_terms={', '.join(search_terms)}",
        f"subreddits={', '.join(subreddits)}\n",
        "# Scraping Settings",
        f"posts_per_search={posts_per_search}",
        f"comments_per_post={comments_per_post}",
        f"sort_method={sort_method}",
        f"time_filter={time_filter}"
    ]

    # Write to file
    with open(config_file, 'w') as f:
        f.write('\n'.join(config_content))

    print(f"Configuration file '{config_file}' has been {'updated' if overwrite else 'generated'} successfully.")



def generate_social_sentiment(industry: str = "",
                              config_file: str = './reddit_config.txt'
                              ) -> list[str]:
    # Get info from ChatGPT
    # Check if the competitor_info file exists
    print("Getting competitor info...", industry)
    competitor_info = gc(industry)
    with open('./competitor_info.txt', 'w') as file:
        file.write(competitor_info)
    with open('./competitor_info.txt', 'r') as file:
        competitor_info = file.read()

    # Parse the competitor_info to extract top_companies and subreddits
    competitor_info = ast.literal_eval(competitor_info)
    top_companies = competitor_info[0]
    subreddits = competitor_info[2]
    # Generate config for scraping
    generate_config(subreddits=subreddits, search_terms=top_companies, config_file=config_file, sort_method='relevant')
    # Do scraping to get csv
    results = ""
    try:
        # Initialize scraper with config file
        scraper = ss.RedditMultiScraper(config_file)

        # Run scraper
        results = scraper.scrape_reddit()

    except FileNotFoundError:
        print("Error: Configuration file 'reddit_config.txt' not found!")
    except KeyError as e:
        print(f"Error: Missing configuration key: {e}")
    except Exception as e:
        print(f"Error: {str(e)}")
    # Use the csv to get sentiment as a string
    to_analyze = ""
    if not results:
        return ""
    to_analyze = pc.parse_reddit_csv(results)
    # Get sentiment
    if not to_analyze:
        return ""
    analyzer = ssa.SocialSentiment(sector=industry)
    sentiment = analyzer.analyze_batch(to_analyze, include_raw=True)
    summary = analyzer.summarize_sentiment(sentiment)
    summary_strings = [
        f"average sentiment: {row['average_sentiment_score']:.3f}, {row['closest_post']}, {row['second_closest_post']}"
        for _, row in summary.iterrows()
    ]
    return summary_strings

def read_sentiment_to_string(file_path='news_sentiment.txt') -> str:
    """Read the news sentiment file and return its contents as a string"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: news_sentiment.txt file not found"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def generate_news_sentiment(industry: str = "") -> str:
    # Get info from ChatGPT
    # Check if the competitor_info file exists
    with open('./competitor_info.txt', 'r') as file:
        competitor_info = file.read()

    # Parse the competitor_info to extract top_companies and subreddits
    competitor_info = ast.literal_eval(competitor_info)
    top_companies = competitor_info[0]
    top_companies_tickers = competitor_info[1]
    # Run general news scraping
    general_news_path = ns.get_multiple_companies_headlines(api_key=os.environ.get('NEWS_SCRAPING_API'), companies=top_companies, output_file='../general_news.csv', headlines_per_company=5)
    # Run financial news scraping
    financial_news_path = fns.get_company_news(top_companies_tickers, max_headlines=5)
    # Run sentiment analysis
    analyzer = nsa.HeadlineSentimentAnalyzer()
    analyzer.process_csv_files(news_csv=general_news_path, financial_csv=financial_news_path)
    # Return sentiment
    sentiment_text = read_sentiment_to_string()
    return sentiment_text

def get_sentiment_context(industry: str = "") -> str:
    context = ""
    social_sentiment = generate_social_sentiment(industry=industry)
    for s in social_sentiment:
        context += s + "\n"
    context += generate_news_sentiment(industry=industry)
    return context


def process_industry_sentiments(industries: list) -> None:
    """
    Iterate over industries, get sentiment context for each, and write to individual files

    Args:
        industries (list): List of industry names to process
    """
    try:
        # Process each industry
        for industry in industries:
            # Clean industry name for filename
            clean_industry = industry.lower().replace(' ', '_').replace('&', 'and')
            filename = f"{clean_industry}_sentiment.txt"

            try:
                # Get sentiment context for the industry
                sentiment_context = get_sentiment_context(industry)

                # Write to industry-specific file
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"=== Sentiment Context for {industry} ===\n\n")
                    f.write(sentiment_context)

                print(f"Successfully wrote sentiment context for {industry} to {filename}")

            except Exception as e:
                print(f"Error processing {industry}: {str(e)}")
                continue

    except Exception as e:
        print(f"Error in processing industries: {str(e)}")
        raise


if __name__ == "__main__":
    # search_terms = ['beigene', 'tango therapeutics', 'allogene therapeutics']
    # subreddits = ['biotech']

    # print(generate_social_sentiment(industry="space"))
    # print(generate_news_sentiment(industry="space"))
    # print(get_sentiment_context("space"))

    industries = [
        'Automotive',
        'Banking',
        'Construction',
        'Education',
        'Energy',
        'Fashion',
        'Food and Beverage',
        'Healthcare',
        'Information Technology',
        'Manufacturing',
        'Media and Entertainment',
        'Real Estate',
        'Retail',
        'Telecommunications',
        'Transportation',
        'Travel and Tourism',
        'Utilities',
        'Wholesale',
        'Not Specified'
    ]
    process_industry_sentiments(industries)

