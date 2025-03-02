#!/usr/bin/env python3
"""
Test script for debugging the EnhancedOddsClient time filtering.

This script runs various tests to understand how the time filtering works
in the get_available_sports_tonight function.
"""
import os
import sys
from dotenv import load_dotenv
from datetime import datetime, timezone, time, timedelta

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from api_test.tool_testing.enhanced_client import EnhancedOddsClient


def format_datetime(dt):
    """Format datetime to a readable string."""
    if dt is None:
        return "None"
    return dt.strftime('%Y-%m-%d %H:%M:%S %Z')


def print_game_info(game, start_time, end_time):
    """Print detailed information about a game and its time window."""
    away_team = game.get('away_team', 'Unknown')
    home_team = game.get('home_team', 'Unknown')
    
    if 'commence_time' in game:
        commence_time_str = game.get('commence_time', 'Unknown')
        try:
            game_time = datetime.fromisoformat(commence_time_str.replace('Z', '+00:00'))
            in_window = start_time <= game_time <= end_time
            print(f"  Game: {away_team} @ {home_team}")
            print(f"  Commence time: {format_datetime(game_time)}")
            print(f"  In window: {in_window}")
            print(f"  Window: {format_datetime(start_time)} to {format_datetime(end_time)}")
            print()
            return game_time, in_window
        except (ValueError, TypeError):
            print(f"  Game: {away_team} @ {home_team}")
            print(f"  Invalid commence time: {commence_time_str}")
            print()
    else:
        print(f"  Game: {away_team} @ {home_team}")
        print(f"  No commence time available")
        print()
    
    return None, False


def print_timeline(start_time, end_time, games):
    """Print a simple ASCII timeline of games."""
    print(f"Timeline from {format_datetime(start_time)} to {format_datetime(end_time)}")
    print("=" * 80)
    
    # Calculate total duration in hours
    duration = (end_time - start_time).total_seconds() / 3600
    scale = 80 / duration  # Scale factor for 80-char width
    
    for game in games:
        if 'commence_time' in game:
            try:
                game_time = datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00'))
                position = int((game_time - start_time).total_seconds() / 3600 * scale)
                
                # Create the timeline
                if 0 <= position < 80:
                    line = " " * position + "X" + " " * (80 - position - 1)
                    print(f"{line} {game.get('away_team', 'Unknown')} @ {game.get('home_team', 'Unknown')} ({format_datetime(game_time)})")
            except (ValueError, TypeError):
                continue
    
    print("=" * 80)
    print(f"{format_datetime(start_time)}" + " " * 30 + f"{format_datetime(end_time)}")


def test_default_behavior(client):
    """Test the default behavior of get_available_sports_tonight."""
    print("\n=== Testing Default Behavior ===\n")
    
    # Get current date in UTC
    now = datetime.now(timezone.utc)
    today = now.date()
    tomorrow = today + timedelta(days=1)
    
    # Default start_time and end_time
    start_time = now
    end_time = datetime.combine(tomorrow, time(6, 0), tzinfo=timezone.utc)
    
    print(f"Current time (UTC): {format_datetime(now)}")
    print(f"Default window: {format_datetime(start_time)} to {format_datetime(end_time)}")
    print()
    
    # Get sports with default parameters
    sports = client.get_available_sports_tonight()
    
    print(f"Found {len(sports['data'])} sports with games in the default window")
    
    # Check a few sports
    for sport in sports['data'][:3]:  # Look at first 3 sports
        print(f"\nSport: {sport['title']} ({sport['key']})")
        print(f"Games count: {sport['games_count']}")
        
        # Get raw data for this sport
        raw_response = client.get_odds(sport['key'], {"regions": "us", "dateFormat": "iso"})
        
        # Count games in window
        games_in_window = []
        for game in raw_response['data']:
            game_time, in_window = print_game_info(game, start_time, end_time)
            if in_window:
                games_in_window.append(game)
        
        print(f"Games actually in window: {len(games_in_window)}")
        
        # Check sample game
        if sport.get('sample_game'):
            sample_game = sport['sample_game']
            print("\nSample game:")
            print_game_info(sample_game, start_time, end_time)
        
        # Print timeline
        print_timeline(start_time, end_time, raw_response['data'])


def test_explicit_time_windows(client):
    """Test with explicit time windows."""
    print("\n=== Testing Explicit Time Windows ===\n")
    
    # Get current date in UTC
    now = datetime.now(timezone.utc)
    today = now.date()
    tomorrow = today + timedelta(days=1)
    
    # Test cases
    test_cases = [
        {
            "name": "Today only",
            "start_time": now,
            "end_time": datetime.combine(today, time(23, 59, 59), tzinfo=timezone.utc)
        },
        {
            "name": "Next 24 hours",
            "start_time": now,
            "end_time": now + timedelta(hours=24)
        },
        {
            "name": "Tomorrow only",
            "start_time": datetime.combine(tomorrow, time(0, 0), tzinfo=timezone.utc),
            "end_time": datetime.combine(tomorrow, time(23, 59, 59), tzinfo=timezone.utc)
        }
    ]
    
    for case in test_cases:
        print(f"\n--- {case['name']} ---\n")
        print(f"Window: {format_datetime(case['start_time'])} to {format_datetime(case['end_time'])}")
        
        # Get sports with explicit time window
        sports = client.get_available_sports_tonight(
            start_time=case['start_time'],
            end_time=case['end_time']
        )
        
        print(f"Found {len(sports['data'])} sports with games in this window")
        
        # Check a sample sport
        if sports['data']:
            sport = sports['data'][0]
            print(f"\nSample sport: {sport['title']} ({sport['key']})")
            print(f"Games count: {sport['games_count']}")
            
            # Check sample game
            if sport.get('sample_game'):
                sample_game = sport['sample_game']
                print("\nSample game:")
                print_game_info(sample_game, case['start_time'], case['end_time'])


def test_nba_games(client):
    """Test specifically with NBA games."""
    print("\n=== Testing NBA Games ===\n")
    
    # Get current date in UTC
    now = datetime.now(timezone.utc)
    today = now.date()
    tomorrow = today + timedelta(days=1)
    
    # Default start_time and end_time
    start_time = now
    end_time = datetime.combine(tomorrow, time(6, 0), tzinfo=timezone.utc)
    
    print(f"Current time (UTC): {format_datetime(now)}")
    print(f"Default window: {format_datetime(start_time)} to {format_datetime(end_time)}")
    print()
    
    # Get raw NBA data
    sport_key = "basketball_nba"
    raw_response = client.get_odds(sport_key, {"regions": "us", "dateFormat": "iso"})
    
    print(f"Total NBA games: {len(raw_response['data'])}")
    
    # Check each game
    games_in_window = []
    for game in raw_response['data']:
        game_time, in_window = print_game_info(game, start_time, end_time)
        if in_window:
            games_in_window.append(game)
    
    print(f"NBA games in window: {len(games_in_window)}")
    
    # Print timeline
    print_timeline(start_time, end_time, raw_response['data'])
    
    # Check if any games are after the window
    games_after_window = []
    for game in raw_response['data']:
        if 'commence_time' in game:
            try:
                game_time = datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00'))
                if game_time > end_time:
                    games_after_window.append(game)
            except (ValueError, TypeError):
                continue
    
    print(f"\nNBA games after window: {len(games_after_window)}")
    for game in games_after_window:
        print_game_info(game, start_time, end_time)


def main():
    """Main function to run tests."""
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        print("Error: ODDS_API_KEY not found in environment variables")
        print("Please create a .env file with your API key: ODDS_API_KEY=your_api_key_here")
        return
    
    # Create client
    client = EnhancedOddsClient(api_key)
    
    try:
        # Run tests
        test_default_behavior(client)
        test_explicit_time_windows(client)
        test_nba_games(client)
        
    except Exception as e:
        print(f"Error during testing: {e}")


if __name__ == "__main__":
    main()
