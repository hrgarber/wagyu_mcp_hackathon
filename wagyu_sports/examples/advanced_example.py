#!/usr/bin/env python3
"""
Advanced example script demonstrating more complex usage of the Wagyu Sports client.

This example shows:
1. Error handling
2. Handling API quota limits
3. Fetching multiple sports and odds
4. Filtering and processing data
"""
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests

from wagyu_sports import OddsClient


def format_datetime(dt_str):
    """Format ISO datetime string to a more readable format."""
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, AttributeError):
        return dt_str


def get_upcoming_games(client, sport_key, hours=24):
    """
    Get upcoming games for a sport within the next X hours.
    
    Args:
        client (OddsClient): The Wagyu Sports client
        sport_key (str): Sport key (e.g., 'basketball_nba')
        hours (int): Number of hours to look ahead
        
    Returns:
        list: List of upcoming games
    """
    try:
        # Get odds with options
        options = {
            "regions": "us",
            "markets": "h2h",
            "oddsFormat": "decimal",
            "dateFormat": "iso"
        }
        
        response = client.get_odds(sport_key, options)
        
        # Calculate cutoff time
        now = datetime.now()
        cutoff = now + timedelta(hours=hours)
        
        # Filter games by commence time
        upcoming_games = []
        for game in response['data']:
            if 'commence_time' in game:
                try:
                    game_time = datetime.fromisoformat(
                        game['commence_time'].replace('Z', '+00:00')
                    )
                    if now <= game_time <= cutoff:
                        upcoming_games.append(game)
                except (ValueError, TypeError):
                    # Skip games with invalid datetime
                    continue
        
        return upcoming_games, response['headers']['x-requests-remaining']
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching odds for {sport_key}: {e}")
        return [], None


def find_best_odds(games):
    """
    Find the best odds for each team across all bookmakers.
    
    Args:
        games (list): List of games with odds
        
    Returns:
        dict: Dictionary mapping team names to their best odds
    """
    best_odds = {}
    
    for game in games:
        home_team = game.get('home_team')
        away_team = game.get('away_team')
        
        if not home_team or not away_team:
            continue
        
        # Initialize best odds for teams if not already present
        if home_team not in best_odds:
            best_odds[home_team] = 0
        if away_team not in best_odds:
            best_odds[away_team] = 0
        
        # Check all bookmakers
        for bookmaker in game.get('bookmakers', []):
            for market in bookmaker.get('markets', []):
                if market.get('key') == 'h2h':
                    for outcome in market.get('outcomes', []):
                        team = outcome.get('name')
                        price = outcome.get('price')
                        
                        if team and price and team in best_odds:
                            best_odds[team] = max(best_odds[team], price)
    
    return best_odds


def main():
    """Main function demonstrating advanced usage."""
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
    
    try:
        # Get available sports
        print("Fetching available sports...")
        sports_response = client.get_sports()
        
        # Check if we have sports data
        if not sports_response['data']:
            print("No sports data available")
            return
        
        print(f"Found {len(sports_response['data'])} sports")
        print(f"Remaining requests: {sports_response['headers']['x-requests-remaining']}")
        
        # Get active sports (in-season)
        active_sports = []
        for sport in sports_response['data']:
            if sport.get('active'):
                active_sports.append(sport)
        
        print(f"Found {len(active_sports)} active sports")
        
        # Process top 3 active sports
        for i, sport in enumerate(active_sports[:3]):
            sport_key = sport.get('key')
            sport_title = sport.get('title')
            
            print(f"\nProcessing {sport_title} ({sport_key})...")
            
            # Get upcoming games
            upcoming_games, remaining = get_upcoming_games(client, sport_key, hours=48)
            
            if not upcoming_games:
                print(f"No upcoming games found for {sport_title}")
                continue
            
            print(f"Found {len(upcoming_games)} upcoming games in the next 48 hours")
            
            # Find best odds
            best_odds = find_best_odds(upcoming_games)
            
            # Display results
            print(f"\nUpcoming {sport_title} games:")
            for game in upcoming_games[:5]:  # Show up to 5 games
                home = game.get('home_team', 'Unknown')
                away = game.get('away_team', 'Unknown')
                time_str = format_datetime(game.get('commence_time', ''))
                print(f"- {away} @ {home} (Start: {time_str})")
                
                # Show bookmakers
                if game.get('bookmakers'):
                    print(f"  Available at {len(game['bookmakers'])} bookmakers")
            
            print(f"\nBest odds for {sport_title} teams:")
            sorted_odds = sorted(best_odds.items(), key=lambda x: x[1], reverse=True)
            for team, odds in sorted_odds[:5]:  # Show top 5 teams by odds
                print(f"- {team}: {odds:.2f}")
            
            # Check remaining requests
            if remaining and int(remaining) < 10:
                print(f"\nWarning: Only {remaining} API requests remaining")
                print("Waiting 5 seconds before next request to avoid rate limiting...")
                time.sleep(5)
            
            print(f"Remaining requests: {remaining}")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
