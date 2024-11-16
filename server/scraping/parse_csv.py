import csv
from datetime import datetime


def parse_reddit_csv(filename):
    """
    Parse a Reddit CSV file and print the title and body of each entry.

    Args:
        filename (str): Path to the CSV file containing Reddit data with fields:
        search_term, subreddit, title, content_type, body, author, score, url, timestamp
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                print("\n=== Post ===")
                print(f"Title: {row['title']}")
                print(f"Subreddit: r/{row['subreddit']}")
                print(f"Author: u/{row['author']}")
                print(f"Score: {row['score']}")
                print(f"Content Type: {row['content_type']}")
                print("\nBody:")
                print(row['body'])
                print("=" * 50)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error parsing CSV: {str(e)}")


if __name__ == "__main__":
    # You can change the filename here
    parse_reddit_csv("../../../reddit_structured_data_20241116_040116.csv")