"""
Python Odds API Client Package

This package provides a client for The Odds API v4, allowing users to fetch
sports betting data including live odds, scores, and event information.
"""

from .odds_client import OddsClient
from .utils import get_next_test_number, save_response, test_odds_api

__all__ = ['OddsClient', 'get_next_test_number', 'save_response', 'test_odds_api']
