#!/usr/bin/env python3
"""
Simple verification script to check imports from the Wagyu Sports client.

This script attempts to import the OddsClient class and create an instance,
which verifies that the package is installed correctly and can be imported.
"""

try:
    print("Attempting to import OddsClient...")
    from wagyu_sports import OddsClient
    print("Successfully imported OddsClient!")
    
    # Try creating an instance
    client = OddsClient("test_key")
    print("Successfully created OddsClient instance!")
    
except ImportError as e:
    print(f"Import Error: {e}")
    
except Exception as e:
    print(f"Other Error: {e}")
