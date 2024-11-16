import yfinance as yf
import pandas as pd
from datetime import datetime
import time


def get_company_news(ticker_symbols, max_headlines=5):
    """
    Get recent news headlines for a list of companies and save to CSV

    Args:
        ticker_symbols (list): List of company ticker symbols
        max_headlines (int): Maximum number of headlines per company

    Returns:
        str: Filename of the created CSV
    """
    # List to store all news items
    all_news = []

    # Get news for each company
    for symbol in ticker_symbols:
        try:
            print(f"Getting news for {symbol}...")
            ticker = yf.Ticker(symbol)
            news = ticker.news[:max_headlines]

            # Process each news item
            for item in news:
                all_news.append({
                    'ticker': symbol,
                    'title': item['title'],
                    'publisher': item.get('publisher', 'N/A'),
                    'date': datetime.fromtimestamp(item['providerPublishTime']).strftime('%Y-%m-%d %H:%M:%S'),
                    'link': item.get('link', 'N/A')
                })

            # Add a small delay to avoid hitting rate limits
            time.sleep(1)

        except Exception as e:
            print(f"Error getting news for {symbol}: {str(e)}")
            continue

    # Convert to DataFrame
    df = pd.DataFrame(all_news)

    # Create filename with timestamp
    filename = f"company_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"\nNews headlines saved to {filename}")

    return filename


# Example usage
if __name__ == "__main__":
    companies = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
    output_file = get_company_news(companies)
    print(f"Data written to: {output_file}")