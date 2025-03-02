#!/usr/bin/env python3
"""
Utility functions for working with the Wagyu Sports client.
"""
import os
import json
import glob
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
from dotenv import load_dotenv

from .odds_client import OddsClient


def get_next_test_number() -> int:
    """
    Get the next sequential test number for the output directory.
    
    This function looks at existing test directories and returns the next number in sequence.
    
    Returns:
        int: Next test number
    """
    # Define the base directory for test outputs
    base_dir = os.path.join(os.getcwd(), "test_outputs")
    
    # Ensure the directory exists
    os.makedirs(base_dir, exist_ok=True)
    
    # Find all test directories
    test_dirs = glob.glob(os.path.join(base_dir, "test*"))
    
    if not test_dirs:
        return 1
    
    # Extract numbers from directory names
    numbers = []
    for dir_path in test_dirs:
        dir_name = os.path.basename(dir_path)
        try:
            # Extract number from "test{number}"
            num = int(dir_name.replace("test", ""))
            numbers.append(num)
        except ValueError:
            continue
    
    # Return next number in sequence
    return max(numbers) + 1 if numbers else 1


def save_response(filename: str, data: Dict[str, Any], test_number: Optional[int] = None) -> str:
    """
    Save API response to a JSON file.
    
    Args:
        filename (str): Name of the file to save
        data (Dict[str, Any]): Data to save
        test_number (int, optional): Test number for directory. If None, uses next available.
        
    Returns:
        str: Path to the saved file
    """
    # Get test number if not provided
    if test_number is None:
        test_number = get_next_test_number()
    
    # Define directory path
    dir_path = os.path.join(os.getcwd(), "test_outputs", f"test{test_number}")
    
    # Ensure directory exists
    os.makedirs(dir_path, exist_ok=True)
    
    # Define file path
    file_path = os.path.join(dir_path, filename)
    
    # Save data to file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    return file_path


def test_wagyu_sports() -> Tuple[str, str]:
    """
    Example function that demonstrates full API workflow.
    
    This function:
    1. Loads the API key from environment variables
    2. Creates an OddsClient instance
    3. Fetches available sports
    4. Fetches NBA odds
    5. Saves responses to files
    
    Returns:
        Tuple[str, str]: Paths to the saved files (sports, odds)
    """
    # Load environment variables
    load_dotenv(dotenv_path="config/.env")
    
    # Get API key
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        raise ValueError("ODDS_API_KEY not found in environment variables")
    
    # Create client
    client = OddsClient(api_key)
    
    # Get test number
    test_number = get_next_test_number()
    
    # Get available sports
    try:
        sports_response = client.get_sports()
        sports_file = save_response("1_available_sports.json", sports_response, test_number)
        print(f"Available sports saved to {sports_file}")
        print(f"Remaining requests: {sports_response['headers']['x-requests-remaining']}")
    except Exception as e:
        print(f"Error fetching sports: {e}")
        return "", ""
    
    # Get NBA odds
    try:
        odds_options = {
            "regions": "us",
            "markets": "h2h,spreads",
            "oddsFormat": "american"
        }
        odds_response = client.get_odds("basketball_nba", odds_options)
        odds_file = save_response("2_nba_odds.json", odds_response, test_number)
        print(f"NBA odds saved to {odds_file}")
        print(f"Remaining requests: {odds_response['headers']['x-requests-remaining']}")
    except Exception as e:
        print(f"Error fetching NBA odds: {e}")
        return sports_file, ""
    
    return sports_file, odds_file


if __name__ == "__main__":
    # Run the test if this file is executed directly
    test_wagyu_sports()
