#!/usr/bin/env python3
"""
Example script for fetching NBA odds using the Wagyu Sports client.

This script demonstrates how to use the Wagyu Sports client to fetch NBA odds
and save the response to a file.
"""
import os
import json
from dotenv import load_dotenv
import requests


def fetch_nba_odds():
    """
    Fetch NBA odds from the sports data API.
    
    This function:
    1. Loads the API key from environment variables
    2. Makes a direct request to the sports data API for NBA odds
    3. Saves the response to a file
    
    Returns:
        str: Path to the saved file
    """
    # Load environment variables
    load_dotenv(dotenv_path="config/.env")
    
    # Get API key
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        print("Error: ODDS_API_KEY not found in environment variables")
        print("Please copy config/.env.example to config/.env and add your API key: ODDS_API_KEY=your_api_key_here")
        return
    
    try:
        # Get NBA odds
        response = requests.get(
            'https://api.the-odds-api.com/v4/sports/basketball_nba/odds',
            params={
                'apiKey': api_key,
                'regions': 'us',
                'markets': 'h2h,spreads',
                'oddsFormat': 'american'
            }
        )
        
        # Check for successful response
        response.raise_for_status()
        
        # Prepare output
        output = {
            'odds': response.json(),
            'remainingRequests': response.headers.get('x-requests-remaining')
        }
        
        # Write response to file
        with open('nba_odds.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print('NBA odds written to nba_odds.json')
        print(f'Remaining requests: {output["remainingRequests"]}')
        
        return 'nba_odds.json'
        
    except requests.exceptions.RequestException as e:
        print(f'Error: {e.response.json() if hasattr(e, "response") else str(e)}')
        return None


if __name__ == "__main__":
    # Run the example if this file is executed directly
    fetch_nba_odds()
