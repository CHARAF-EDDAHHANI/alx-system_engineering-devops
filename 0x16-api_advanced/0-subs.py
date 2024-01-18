#!/usr/bin/python3
"""
This module provides a function to retrieve the number of subscribers for a subreddit.
"""

import requests

HEADERS = {"User-Agent": "MyCustomUserAgent/1.0"}

def number_of_subscribers(subreddit):
    """
    Retrieve the number of subscribers for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.

    Returns:
        int: The number of subscribers, or None if an error occurs.
    """
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    response = requests.get(url, headers=HEADERS, allow_redirects=False)

    try:
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
        return data["data"]["subscribers"]
    except requests.exceptions.RequestException as e:
        # Print the error message for debugging
        print(f"Error: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        subreddit_name = sys.argv[1]
        subscribers = number_of_subscribers(subreddit_name)

        if subscribers is not None:
            if subscribers > 0:
                print(f"The subreddit '{subreddit_name}' has {subscribers} subscribers.")
            else:
                print(f"The subreddit '{subreddit_name}' has 0 subscribers.")
        else:
            print(f"Failed to retrieve subscriber count for subreddit '{subreddit_name}'.")
