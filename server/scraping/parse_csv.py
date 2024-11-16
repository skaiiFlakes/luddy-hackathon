import csv
from datetime import datetime


def parse_reddit_csv(filename: str = ""):
    """
    Parse a Reddit CSV file and return a list of strings with the title and body of each entry.

    Args:
        filename (str): Path to the CSV file containing Reddit data with fields:
        search_term, subreddit, title, content_type, body, author, score, url, timestamp

    Returns:
        List[str]: List of strings with the title and body of each entry.
    """
    if not filename:
        return ""
    posts = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                post = f"Title: {row['title']}\nBody: {row['body']}"
                posts.append(post)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error parsing CSV: {str(e)}")

    return posts


if __name__ == "__main__":
    # You can change the filename here
    posts = parse_reddit_csv("../scraping/reddit_structured_data_20241116_130352.csv")
    for post in posts:
        print(post)
        print("=" * 50)