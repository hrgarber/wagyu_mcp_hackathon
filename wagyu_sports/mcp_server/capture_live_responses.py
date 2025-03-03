#!/usr/bin/env python3
"""
Script to capture live API responses from the Odds API.

This script makes live API calls and saves the responses to JSON files
in the mocks_live directory. These captures can be used for creating
updated mock data for testing.

IMPORTANT: Each live API call costs money. Use sparingly.
"""
import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import from wagyu_sports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from wagyu_sports.odds_client import OddsClient

async def capture_response(client, method_name, filename, **kwargs):
    """
    Capture a response from the API and save it to a file.
    
    Args:
        client: The OddsClient instance
        method_name: The name of the method to call
        filename: The name of the file to save the response to
        **kwargs: Arguments to pass to the method
    """
    print(f"Calling {method_name} with {kwargs}...")
    
    # Call the method
    method = getattr(client, method_name)
    result = method(**kwargs)
    
    # Add metadata
    response = {
        "_metadata": {
            "captured_at": datetime.now().isoformat(),
            "method": method_name,
            "parameters": kwargs
        },
        "data": result
    }
    
    # Save to file
    output_path = Path(__file__).parent / "mocks_live" / filename
    with open(output_path, "w") as f:
        json.dump(response, f, indent=2)
    
    print(f"Response saved to {output_path}")
    return result

async def main():
    """Run the capture script."""
    # Get API key from environment
    api_key = os.environ.get("ODDS_API_KEY")
    if not api_key:
        print("Error: ODDS_API_KEY environment variable is not set")
        sys.exit(1)
    
    print("=" * 80)
    print("Wagyu Sports Live API Response Capture")
    print("=" * 80)
    print()
    print("WARNING: This script makes live API calls that cost money.")
    print("Only run this script when necessary.")
    print()
    
    # Initialize client
    client = OddsClient(api_key)
    
    # Capture sports list
    await capture_response(
        client, 
        "get_sports", 
        "sports_list_live.json",
        all_sports=True
    )
    
    # Capture NBA odds
    await capture_response(
        client, 
        "get_odds", 
        "nba_games_live.json",
        sport="basketball_nba",
        options={
            "regions": "us",
            "markets": "h2h,spreads"
        }
    )
    
    # Capture soccer odds
    await capture_response(
        client, 
        "get_odds", 
        "soccer_epl_live.json",
        sport="soccer_epl",
        options={
            "regions": "us,uk",
            "markets": "h2h,spreads,totals"
        }
    )
    
    # Print quota information
    print("\nQuota Information:")
    print(f"Remaining requests: {client.remaining_requests}")
    print(f"Used requests: {client.used_requests}")
    
    # Save quota information
    quota_info = {
        "_metadata": {
            "captured_at": datetime.now().isoformat()
        },
        "remaining_requests": client.remaining_requests,
        "used_requests": client.used_requests
    }
    
    quota_path = Path(__file__).parent / "mocks_live" / "quota_info_live.json"
    with open(quota_path, "w") as f:
        json.dump(quota_info, f, indent=2)
    
    print(f"Quota information saved to {quota_path}")
    
    print("\nCapture complete!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCapture stopped by user.")
    except Exception as e:
        print(f"\nError: {e}")
