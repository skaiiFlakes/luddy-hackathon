import os
import praw
import pandas as pd
from datetime import datetime
import time
from typing import List, Optional
from itertools import product

from dotenv import load_dotenv
load_dotenv()

class RedditMultiScraper:
    @staticmethod
    def load_config(config_file: str) -> dict:
        """
        Load configuration from a text file
        """
        config = {}
        with open(config_file, 'r') as f:
            for line in f:
                # Skip comments and empty lines
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=')
                    key = key.strip()
                    value = value.strip()

                    # Handle lists (comma-separated values)
                    if key in ['search_terms', 'subreddits']:
                        config[key] = [v.strip() for v in value.split(',')]
                    # Handle integers
                    elif value.isdigit():
                        config[key] = int(value)
                    # Handle strings
                    else:
                        config[key] = value
        return config

    def __init__(self, config_file: str):
        """
        Initialize Reddit scraper with credentials from config file
        """
        try:
            config = self.load_config(config_file)
            self.reddit = praw.Reddit(
                client_id=os.environ.get('REDDIT_CLIENT_ID'),
                client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                user_agent=os.environ.get('REDDIT_USER_AGENT')
            )
            # Store other config parameters as instance variables
            self.search_terms = config.get('search_terms', [])
            self.subreddits = config.get('subreddits', [])
            self.posts_per_search = config.get('posts_per_search', 5)
            self.comments_per_post = config.get('comments_per_post', 4)
            self.sort_method = config.get('sort_method', 'hot')
            self.time_filter = config.get('time_filter', 'all')

        except Exception as e:
            raise Exception(f"Error initializing scraper: {str(e)}")

    def get_comments(self, post, max_comments: int = None) -> List[dict]:
        """
        Extract comments from a post
        """
        comments_list = []

        try:
            # Replace "More Comments" with actual comments
            post.comments.replace_more(limit=None)

            # Get all comments as flat list
            all_comments = post.comments.list()

            # Sort by score and limit if specified
            all_comments.sort(key=lambda x: x.score, reverse=True)
            if max_comments:
                all_comments = all_comments[:max_comments]

            # Process comments
            for comment in all_comments:
                try:
                    if comment.body != "[deleted]" and comment.body != "[removed]":
                        comment_dict = {
                            "body": comment.body,
                            "score": comment.score,
                            "author": str(comment.author),
                        }
                        comments_list.append(comment_dict)

                except Exception as e:
                    continue

        except Exception as e:
            print(f"Error getting comments: {str(e)}")

        return comments_list

    def scrape_reddit(self) -> str:
        """
        Scrape Reddit posts and comments using configuration parameters
        """
        structured_data = []
        total_combinations = len(self.search_terms) * len(self.subreddits)
        current_combination = 0

        for term, subreddit in product(self.search_terms, self.subreddits):
            current_combination += 1
            print(f"\nProgress: {current_combination}/{total_combinations}")
            print(f"Searching for '{term}' in r/{subreddit}")

            try:
                subreddit_obj = self.reddit.subreddit(subreddit)

                if self.sort_method == "hot":
                    posts = subreddit_obj.hot(limit=self.posts_per_search)
                elif self.sort_method == "new":
                    posts = subreddit_obj.new(limit=self.posts_per_search)
                elif self.sort_method == "top":
                    posts = subreddit_obj.top(time_filter=self.time_filter, limit=self.posts_per_search)
                else:
                    posts = subreddit_obj.search(term, sort=self.sort_method, time_filter=self.time_filter,
                                                 limit=self.posts_per_search)

                posts_found = 0
                for post in posts:
                    if self.sort_method in ["hot", "new", "top"] and term.lower() not in post.title.lower():
                        continue

                    try:
                        # Get post information
                        post_content = post.selftext if post.selftext and post.selftext not in ["[deleted]",
                                                                                                "[removed]"] else ""

                        if post_content:  # Add post content as first entry
                            structured_data.append({
                                "search_term": term,
                                "subreddit": subreddit,
                                "title": post.title,
                                "content_type": "post",
                                "body": post_content,
                                "author": str(post.author),
                                "score": post.score,
                                "url": post.url,
                                "timestamp": datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                            })

                        # Get comments
                        comments = self.get_comments(post, max_comments=self.comments_per_post)

                        # Add each comment as a separate entry with the same title
                        for comment in comments:
                            structured_data.append({
                                "search_term": term,
                                "subreddit": subreddit,
                                "title": post.title,
                                "content_type": "comment",
                                "body": comment["body"],
                                "author": comment["author"],
                                "score": comment["score"],
                                "url": post.url,
                                "timestamp": datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                            })

                        posts_found += 1
                        print(f"Processed post {posts_found} with {len(comments)} comments")

                    except Exception as e:
                        print(f"Error processing post: {str(e)}")
                        continue

                print(f"Completed: Found {posts_found} posts for '{term}' in r/{subreddit}")
                time.sleep(1)  # Be nice to Reddit's servers

            except Exception as e:
                print(f"Error searching {subreddit} for {term}: {str(e)}")
                continue

            time.sleep(1)

        # Create DataFrame
        df = pd.DataFrame(structured_data)

        if df.empty:
            print("No data found matching the search criteria.")
            return df

        # Save to CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"reddit_structured_data_{timestamp}.csv"
        df.to_csv(filename, index=False, encoding='utf-8')

        # Print summary
        print(f"\nFinal Summary:")
        print(f"- Total entries: {len(df)}")
        print(f"- Unique posts: {df['title'].nunique()}")
        print(f"- Posts with content: {len(df[df['content_type'] == 'post'])}")
        print(f"- Total comments: {len(df[df['content_type'] == 'comment'])}")
        print(f"- Output saved to: {filename}")

        # Display distribution
        print("\nEntries per search term:")
        print(df.groupby('search_term').size())
        print("\nEntries per subreddit:")
        print(df.groupby('subreddit').size())

        # return df
        return filename


def main():
    try:
        # Initialize scraper with config file
        scraper = RedditMultiScraper(r"/home/ngoh/Luddy_Hackathon/scraping_config.txt")

        # Run scraper
        results = scraper.scrape_reddit()

    except FileNotFoundError:
        print("Error: Configuration file 'reddit_config.txt' not found!")
    except KeyError as e:
        print(f"Error: Missing configuration key: {e}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
