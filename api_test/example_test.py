#!/usr/bin/env python3
"""
Example script demonstrating how to use the Python Odds API client.
"""
import os
from dotenv import load_dotenv
from python_odds_api import OddsClient


def main():
    """
    Main function demonstrating the use of the Odds API client.
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        print("Error: ODDS_API_KEY not found in environment variables")
        print("Please create a .env file with your API key: ODDS_API_KEY=your_api_key_here")
        return
    
    # Create client
    client = OddsClient(api_key)
    
    # Get available sports
    try:
        print("Fetching available sports...")
        sports_response = client.get_sports()
        
        print(f"\nAvailable sports: {len(sports_response['data'])}")
        print("Sample sports:")
        for sport in sports_response['data'][:5]:  # Show first 5 sports
            print(f"- {sport.get('title', 'Unknown')}: {sport.get('key', 'Unknown')}")
        
        print(f"\nRemaining requests: {sports_response['headers']['x-requests-remaining']}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
