#!/usr/bin/env python3
"""
Simple test script to verify imports from the Python Odds API client.
"""

try:
    print("Attempting to import OddsClient...")
    from python_odds_api import OddsClient
    print("Successfully imported OddsClient!")
    
    # Try creating an instance
    client = OddsClient("test_key")
    print("Successfully created OddsClient instance!")
    
except ImportError as e:
    print(f"Import Error: {e}")
    
except Exception as e:
    print(f"Other Error: {e}")
