"""
Authentication and data fetching script for Strava.

This script handles authentication with the Strava API using tokens
and provides functions to fetch activity data.
"""

from typing import List, Dict
from stravalib import Client
from utils.token_utils import load_tokens, refresh_tokens

def get_strava_client() -> Client:
    """
    Get an authenticated Strava client.

    Returns:
        Client: An authenticated Strava client instance.

    Raises:
        RuntimeError: If no tokens are found or the tokens are invalid.
    """
    tokens = load_tokens()
    if not tokens:
        raise RuntimeError("Tokens not found. You need to authenticate first.")
    
    client = Client()
    tokens = refresh_tokens(client, tokens)
    client.access_token = tokens['access_token']
    client.refresh_token = tokens['refresh_token']
    client.token_expires_at = tokens['expires_at']
    return client