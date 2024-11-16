from scraping import parse_csv as pc
from scraping import social_scraping as ss
from sentiment import social_sentiment_analysis as ssa

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

    # Check if file exists and read existing credentials
    existing_credentials = {
        'CLIENT_ID': '',
        'CLIENT_SECRET': '',
        'USER_AGENT': 'sentiment/1.0'
    }

    try:
        with open(config_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    if key in existing_credentials:
                        existing_credentials[key] = value
            print(f"Found existing configuration file: {config_file}")
            if not overwrite:
                print("Preserving existing API credentials...")
    except FileNotFoundError:
        print(f"No existing configuration file found. Creating new file: {config_file}")

    # Create configuration content
    config_content = [
        "# Reddit API Credentials",
        f"CLIENT_ID={existing_credentials['CLIENT_ID']}",
        f"CLIENT_SECRET={existing_credentials['CLIENT_SECRET']}",
        f"USER_AGENT={existing_credentials['USER_AGENT']}\n",
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
                              top_companies: list[str] = [],
                              subreddits: list[str] = [],
                              search_terms: list[str] = [],
                              config_file: str = './reddit_config.txt'
                              ) -> list[str]:
    # Generate config for scraping
    generate_config(subreddits=subreddits, search_terms=search_terms, config_file=config_file, sort_method='relevant')
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
    analyzer = ssa.SocialSentiment(sector='tech')
    sentiment = analyzer.analyze_batch(to_analyze, include_raw=True)
    summary = analyzer.summarize_sentiment(sentiment)
    summary_strings = [
        f"average sentiment: {row['average_sentiment_score']:.3f}, {row['closest_post']}, {row['second_closest_post']}"
        for _, row in summary.iterrows()
    ]
    return summary_strings


if __name__ == "__main__":
    search_terms = ['spacex', 'L3Harris', 'NextNav']
    subreddits = ['space']

    print(generate_social_sentiment(search_terms=search_terms, subreddits=subreddits))
