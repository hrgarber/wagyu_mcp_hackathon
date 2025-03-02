#!/usr/bin/env python3
"""
Verification script to check the installation and functionality of the Wagyu Sports client.

This script:
1. Checks if the required dependencies are installed
2. Verifies that the API key is set in the environment
3. Runs a simple test to fetch sports data
"""
import os
import sys
import importlib.util


def check_dependency(package_name):
    """Check if a Python package is installed."""
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print(f"Error: {package_name} is not installed.")
        print(f"Please install it using: pip install {package_name}")
        return False
    return True


def main():
    """Main function to run tests."""
    # Check dependencies
    dependencies = ["requests", "dotenv"]
    all_installed = True
    
    for dep in dependencies:
        if not check_dependency(dep):
            all_installed = False
    
    if not all_installed:
        print("\nPlease install all required dependencies and try again.")
        print("You can install them using: pip install -r build/requirements.txt")
        return
    
    # Now that we know dependencies are installed, import them
    from dotenv import load_dotenv
    
    # Check for API key
    load_dotenv(dotenv_path="config/.env")
    api_key = os.getenv("ODDS_API_KEY")
    
    if not api_key:
        print("Error: ODDS_API_KEY not found in environment variables.")
        print("Please copy config/.env.example to .env and add your API key: ODDS_API_KEY=your_api_key_here")
        return
    
    # Try to import the client
    try:
        from wagyu_sports import OddsClient
        
        # Create client
        client = OddsClient(api_key)
        
        # Test getting sports
        print("Testing API connection by fetching available sports...")
        response = client.get_sports()
        
        # Check response
        if "data" in response and isinstance(response["data"], list):
            sport_count = len(response["data"])
            print(f"Success! Fetched {sport_count} available sports.")
            print(f"Remaining API requests: {response['headers']['x-requests-remaining']}")
            
            # Show a few sports as example
            if sport_count > 0:
                print("\nSample sports:")
                for sport in response["data"][:3]:  # Show first 3 sports
                    print(f"- {sport.get('title', 'Unknown')}: {sport.get('key', 'Unknown')}")
            
            print("\nThe Wagyu Sports client is working correctly!")
        else:
            print("Error: Unexpected response format from the API.")
            print("Response:", response)
    
    except ImportError:
        print("Error: Could not import the Wagyu Sports client.")
        print("Make sure the package is installed correctly.")
    
    except Exception as e:
        print(f"Error during API test: {e}")


if __name__ == "__main__":
    main()
