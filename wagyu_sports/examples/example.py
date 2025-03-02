#!/usr/bin/env python3
"""
Example script demonstrating how to use the Wagyu Sports client.
"""
import os
from dotenv import load_dotenv
from wagyu_sports import OddsClient


def main():
    """
    Main function demonstrating the use of the Wagyu Sports client.
    """
    # Load environment variables
    load_dotenv(dotenv_path="config/.env")
    
    # Get API key
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        print("Error: ODDS_API_KEY not found in environment variables")
        print("Please copy config/.env.example to config/.env and add your API key: ODDS_API_KEY=your_api_key_here")
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
        
        # Get a sport key for the next request
        sport_key = None
        for sport in sports_response['data']:
            if sport.get('title') == 'NBA':
                sport_key = sport.get('key')
                break
        
        if not sport_key:
            # If NBA is not found, use the first available sport
            sport_key = sports_response['data'][0].get('key') if sports_response['data'] else None
        
        if not sport_key:
            print("\nNo sports available to fetch odds")
            return
        
        # Get odds for the selected sport
        print(f"\nFetching odds for {sport_key}...")
        odds_options = {
            "regions": "us",
            "markets": "h2h",
            "oddsFormat": "decimal"
        }
        odds_response = client.get_odds(sport_key, odds_options)
        
        games_count = len(odds_response['data'])
        print(f"\nFetched odds for {games_count} games")
        
        if games_count > 0:
            print("\nSample games:")
            for game in odds_response['data'][:3]:  # Show first 3 games
                home_team = game.get('home_team', 'Unknown')
                away_team = game.get('away_team', 'Unknown')
                commence_time = game.get('commence_time', 'Unknown')
                print(f"- {away_team} @ {home_team} (Start: {commence_time})")
                
                # Print sample odds from first bookmaker if available
                if game.get('bookmakers') and len(game.get('bookmakers')) > 0:
                    bookmaker = game.get('bookmakers')[0]
                    print(f"  Odds from {bookmaker.get('title', 'Unknown')}:")
                    
                    for market in bookmaker.get('markets', []):
                        if market.get('key') == 'h2h':
                            print("  Moneyline:")
                            for outcome in market.get('outcomes', []):
                                print(f"    {outcome.get('name', 'Unknown')}: {outcome.get('price', 'Unknown')}")
        
        print(f"\nRemaining requests: {odds_response['headers']['x-requests-remaining']}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
