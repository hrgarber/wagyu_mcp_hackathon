#!/usr/bin/env python3
"""
Simple script to test importing the Python Odds API client.
"""

try:
    from python_odds_api import OddsClient
    print("Success! The Python Odds API client was imported correctly.")
except ImportError as e:
    print(f"Error importing the Python Odds API client: {e}")
