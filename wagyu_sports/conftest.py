"""
Configuration file for pytest.

This file sets up the Python path for tests to ensure imports work correctly.
"""
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
