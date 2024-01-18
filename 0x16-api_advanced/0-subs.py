#!/usr/bin/python3
"""
This module provides a recursive function to retrieve the titles of all hot articles for a given subreddit.
"""

import requests

HEADERS = {"User-Agent": "MyCustomUserAgent/1.0"}

def recurse(subreddit, hot_list=[], after=None):
    """
    Recursive function to retrieve titles of hot articles from Reddit API.

    Args:
        subreddit (str): The subreddit to search.
        hot_list (list): List to store titles (default is an empty list).
        after (str): Token for pagination (default is None).

    Returns:
        List of titles if successful, None otherwise.
    """
    url = f'https://www.reddit.com/r/{subreddit}/hot.json'
    params = {'limit': 100, 'after': after}
    response = requests.get(url, headers=HEADERS, params=params, allow_redirects=False)

    if response.status_code == 200:
        data = response.json().get('data', {})
        children = data.get('children', [])

        for child in children:
            title = child.get('data', {}).get('title', '')
            hot_list.append(title)

        after = data.get('after')
        if after:
            # Recursively call the function for the next page
            recurse(subreddit, hot_list, after)
        else:
            return hot_list

    else:
        # If the subreddit is not valid or no results are found, return None
        print(f"Error: {response.status_code}")
        return None

# Example usage:
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        result = recurse(sys.argv[1])
        if result is not None:
            print(len(result))
        else:
            print("None")
