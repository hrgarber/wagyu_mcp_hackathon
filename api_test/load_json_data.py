#!/usr/bin/env python3
"""
Script to load JSON data from the test4 directory into variables.
"""
import json
import os

def load_json_files():
    """
    Load the JSON files from the test4 directory into variables.
    
    Returns:
        tuple: A tuple containing (available_sports, nba_odds)
    """
    # Define the base directory path
    base_dir = "/Users/harrisongarber/Documents/hackathon/wagyu_mcp_hackathon/api_test/test_outputs/test4"
    
    # Define file paths
    sports_file = os.path.join(base_dir, "1_available_sports.json")
    odds_file = os.path.join(base_dir, "2_nba_odds.json")
    
    # Load the JSON files
    with open(sports_file, 'r') as f:
        available_sports = json.load(f)
    
    with open(odds_file, 'r') as f:
        nba_odds = json.load(f)
    
    return available_sports, nba_odds

def print_summary(available_sports, nba_odds):
    """
    Print a summary of the loaded data.
    
    Args:
        available_sports (dict): The available sports data
        nba_odds (dict): The NBA odds data
    """
    # Print summary of available sports
    sport_count = len(available_sports.get('data', []))
    print(f"Loaded {sport_count} available sports")
    
    # Print the first few sports as an example
    print("\nSample sports:")
    for sport in available_sports.get('data', [])[:3]:
        print(f"- {sport.get('title')}: {sport.get('description')}")
    
    # Print summary of NBA odds
    games_count = len(nba_odds.get('data', []))
    print(f"\nLoaded odds for {games_count} NBA games")
    
    # Print the first few games as an example
    print("\nSample games:")
    for game in nba_odds.get('data', [])[:3]:
        home_team = game.get('home_team')
        away_team = game.get('away_team')
        commence_time = game.get('commence_time')
        print(f"- {away_team} @ {home_team} (Start: {commence_time})")
        
        # Print sample odds from first bookmaker if available
        if game.get('bookmakers') and len(game.get('bookmakers')) > 0:
            bookmaker = game.get('bookmakers')[0]
            print(f"  Odds from {bookmaker.get('title')}:")
            
            for market in bookmaker.get('markets', []):
                if market.get('key') == 'h2h':
                    print("  Moneyline:")
                    for outcome in market.get('outcomes', []):
                        print(f"    {outcome.get('name')}: {outcome.get('price')}")
        print()

if __name__ == "__main__":
    # Load the JSON files
    available_sports, nba_odds = load_json_files()
    
    # Print a summary of the loaded data
    print_summary(available_sports, nba_odds)
    
    # The variables are now available for further use
    print("JSON data loaded successfully and ready for use.")
    print("Variables:")
    print("- available_sports: Contains data about available sports")
    print("- nba_odds: Contains NBA odds data")