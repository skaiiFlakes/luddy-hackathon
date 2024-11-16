import requests
import csv
import time
import pandas as pd

def get_industry_headlines(api_key: str, industry: str, output_file: str = 'industry_headlines.csv',
                         page_size: int = 20) -> list[str]:
    """
    Fetch headlines for a specific industry from US news sources and save to CSV.

    Args:
        api_key (str): NewsAPI API key
        industry (str): Industry to search for (e.g., "artificial intelligence", "banking")
        output_file (str): Path to output CSV file
        page_size (int): Number of articles to fetch (max 100)

    Returns:
        list[str]: List of headlines
    """
    base_url = "https://newsapi.org/v2/everything"

    # Construct query to focus on US industry news
    query = f"{industry} AND (industry OR market OR sector) AND (US OR USA OR America)"

    params = {
        "q": query,
        "language": "en",
        "pageSize": page_size,
        "sortBy": "relevancy",
        "apiKey": api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        data = response.json()

        if data.get("status") == "error":
            raise ValueError(f"API Error: {data.get('message', 'Unknown error')}")

        headlines = []

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow(['headline'])  # Single column header

            for article in data.get("articles", []):
                headline = article.get("title", "").strip()

                if headline:  # Skip empty headlines
                    headlines.append(headline)
                    writer.writerow([headline])

                time.sleep(0.1)  # Rate limiting

        print(f"Successfully wrote {len(headlines)} headlines to {output_file}")
        return headlines

    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch headlines: {str(e)}")
    except IOError as e:
        raise IOError(f"Failed to write to CSV file: {str(e)}")

def get_multiple_companies_headlines(api_key: str, companies: list[str],
                                     output_file: str = './general_news.csv',
                                     headlines_per_company: int = 5) -> str:
    """
    Fetch headlines for multiple companies and save all to a single CSV file.

    Args:
        api_key (str): NewsAPI API key
        companies (list[str]): List of company names to fetch headlines for
        output_file (str): Path to output CSV file
        headlines_per_company (int): Number of headlines to fetch per company

    Returns:
        pd.DataFrame: DataFrame containing all headlines with company labels
    """
    all_headlines = []

    try:
        for company in companies:
            print(f"\nFetching headlines for {company}...")

            # Get headlines for this company
            headlines = get_industry_headlines(
                api_key=api_key,
                industry=company,
                page_size=headlines_per_company,
                output_file='temp.csv'  # Temporary file, will be overwritten
            )

            # Add company and headlines to our collection
            all_headlines.extend([[company, headline] for headline in headlines])

            print(f"Found {len(headlines)} headlines for {company}")

            # Add delay between API calls to respect rate limits
            time.sleep(1)

        # Create DataFrame with all results
        df = pd.DataFrame(all_headlines, columns=['company', 'headline'])

        # Save to CSV
        df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)

        print(f"\nSuccessfully wrote {len(df)} total headlines to {output_file}")
        print(f"Headlines per company:")
        print(df['company'].value_counts().to_string())

        # return df
        return output_file

    except Exception as e:
        print(f"Error processing companies: {str(e)}")
        # If we have partial results, save them
        if all_headlines:
            df = pd.DataFrame(all_headlines, columns=['company', 'headline'])
            backup_file = 'backup_' + output_file
            df.to_csv(backup_file, index=False, quoting=csv.QUOTE_ALL)
            print(f"Saved partial results to {backup_file}")
        raise



# Example usage:
if __name__ == "__main__":
    API_KEY = ""

    # List of companies to fetch headlines for
    companies = [
        "Apple",
        "Microsoft",
        "Tesla",
        "Amazon",
        "Google"
    ]

    try:
        # Get headlines for all companies
        headlines_df = get_multiple_companies_headlines(
            api_key=API_KEY,
            companies=companies,
            output_file='../general_news.csv',
            headlines_per_company=20
        )

        # Print sample of results for each company
        for company in companies:
            company_headlines = headlines_df[headlines_df['company'] == company]
            print(f"\nSample headlines for {company}:")
            print(company_headlines['headline'].head(3).to_string())
            print('-' * 80)

    except Exception as e:
        print(f"Error: {str(e)}")