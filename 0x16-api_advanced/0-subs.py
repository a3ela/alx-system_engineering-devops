#!/usr/bin/python3
"""Function to query subscribers on a given Reddit subreddit."""

import requests


def number_of_subscribers(subreddit):
    """
    Queries the Reddit API and returns the number of
    subscribers for a given subreddit.
    If an invalid subreddit is given, returns 0.

    Args:
        subreddit (str): The name of the subreddit.

    Returns:
        int: The number of subscribers, or 0 if the subreddit is invalid.
    """
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {
        'User-Agent': 'linux:0x16.api.advanced:v1.0.0 \
        (by /u/Few_Dragonfruit_9466)'
    }

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            results = response.json().get('data')
            return results.get('subscribers')
        else:
            return 0
    except requests.RequestException:
        return 0
