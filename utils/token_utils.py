"""
Token management utilities for Strava API.

This module provides functionality to load, save, and refresh tokens
needed for authenticating with the Strava API.
"""

import os
import time
import json
from typing import Optional, Dict
from stravalib.client import Client

TOKEN_FILE = 'strava_tokens.json'


def load_tokens() -> Optional[Dict[str, str]]:
    """
    Load tokens from a file.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing token data, or None if the file does not exist.
    """
    try:
        with open(TOKEN_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def save_tokens(tokens: Dict[str, str]) -> None:
    """
    Save tokens to a file.

    Args:
        tokens (Dict[str, str]): A dictionary containing token data.
    """
    with open(TOKEN_FILE, 'w') as file:
        json.dump(tokens, file)


def refresh_tokens(client: Client, tokens: Dict[str, str]) -> Dict[str, str]:
    """
    Refresh the access token if it has expired.

    Args:
        client (Client): The Strava client instance.
        tokens (Dict[str, str]): A dictionary containing the current token data.

    Returns:
        Dict[str, str]: The updated token data.

    Raises:
        ValueError: If CLIENT_ID or CLIENT_SECRET is missing from environment variables.
    """
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    if not client_id or not client_secret:
        raise ValueError("CLIENT_ID or CLIENT_SECRET is missing in environment variables.")

    if time.time() > tokens['expires_at']:
        print("Refreshing access token...")
        refresh_response = client.refresh_access_token(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=tokens['refresh_token']
        )
        tokens.update({
            'access_token': refresh_response['access_token'],
            'refresh_token': refresh_response['refresh_token'],
            'expires_at': refresh_response['expires_at']
        })
        save_tokens(tokens)
    else:
        print("Access token is still valid.")
    return tokens
