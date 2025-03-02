#!/usr/bin/env python3
"""
Example script demonstrating how to use the Enhanced Odds API client.

This script shows how to use the get_available_sports_tonight function
to find sports with games available for betting tonight in the US region,
with proper timezone handling.
"""
import os
import sys
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import pytz

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from api_test.tool_testing.enhanced_client import EnhancedOddsClient


def format_datetime(dt_str, timezone_str=None):
    """Format ISO datetime string to a more readable format."""
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        if timezone_str:
            try:
                local_tz = pytz.timezone(timezone_str)
                dt = dt.astimezone(local_tz)
            except pytz.exceptions.UnknownTimeZoneError:
                pass
        return dt.strftime('%Y-%m-%d %H:%M:%S %Z')
    except (ValueError, AttributeError):
        return dt_str


def display_sports(sports_data, title):
    """Display sports data in a formatted way."""
    print(f"\n{title}:")
    
    # Display time window information
    if 'time_window' in sports_data:
        window = sports_data['time_window']
        print(f"Time window: {format_datetime(window['start_time_local'])} to {format_datetime(window['end_time_local'])}")
        print(f"Timezone: {window['timezone']}")
    
    for sport in sports_data['data']:
        print(f"\n- {sport['title']} ({sport['key']}): {sport['games_count']} games")
        
        # Show a sample game if available
        if sport.get('sample_game'):
            game = sport['sample_game']
            home_team = game.get('home_team', 'Unknown')
            away_team = game.get('away_team', 'Unknown')
            
            # Use local time if available, otherwise use UTC time
            if 'commence_time_local' in game:
                commence_time = format_datetime(game.get('commence_time_local'))
                print(f"  Sample game: {away_team} @ {home_team} (Start: {commence_time})")
            else:
                commence_time = format_datetime(game.get('commence_time', 'Unknown'))
                print(f"  Sample game: {away_team} @ {home_team} (Start: {commence_time} UTC)")
            
            # Show sample odds from first bookmaker if available
            if game.get('bookmakers') and len(game.get('bookmakers')) > 0:
                bookmaker = game.get('bookmakers')[0]
                print(f"  Odds from {bookmaker.get('title', 'Unknown')}:")
                
                for market in bookmaker.get('markets', []):
                    if market.get('key') == 'h2h':
                        print("  Moneyline:")
                        for outcome in market.get('outcomes', []):
                            print(f"    {outcome.get('name', 'Unknown')}: {outcome.get('price', 'Unknown')}")
    
    print(f"\nRemaining requests: {sports_data['headers']['x-requests-remaining']}")


def main():
    """
    Main function demonstrating the use of the Enhanced Odds API client.
    """
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        print("Error: ODDS_API_KEY not found in environment variables")
        print("Please create a .env file with your API key: ODDS_API_KEY=your_api_key_here")
        return
    
    # Create enhanced client
    client = EnhancedOddsClient(api_key)
    
    try:
        # Example 1: Default behavior - using local timezone (America/Los_Angeles)
        print("Example 1: Fetching sports available for betting tonight in the US region (local timezone)...")
        tonight_sports = client.get_available_sports_tonight(region="us")
        display_sports(tonight_sports, f"Found {len(tonight_sports['data'])} sports with games tonight")
        
        # Example 2: Using a specific timezone (Eastern Time)
        print("\n\nExample 2: Fetching sports available for betting tonight in Eastern Time...")
        et_sports = client.get_available_sports_tonight(
            region="us",
            timezone_str="America/New_York"
        )
        display_sports(et_sports, f"Found {len(et_sports['data'])} sports with games tonight (Eastern Time)")
        
        # Example 3: Custom time window - next 3 hours in local timezone
        print("\n\nExample 3: Fetching sports with games in the next 3 hours...")
        
        # Get current time in local timezone
        now_local = datetime.now(pytz.timezone('America/Los_Angeles'))
        end_time_local = now_local + timedelta(hours=3)
        
        # Get sports with games in the next 3 hours
        next_3_hours_sports = client.get_available_sports_tonight(
            region="us",
            start_time=now_local,
            end_time=end_time_local
        )
        display_sports(next_3_hours_sports, f"Found {len(next_3_hours_sports['data'])} sports with games in the next 3 hours")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
