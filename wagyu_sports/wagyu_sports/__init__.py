"""
Wagyu Sports Package

This package provides a client for sports betting data, allowing users to fetch
sports betting data including live odds, scores, and event information.
"""

from .odds_client import OddsClient
from .utils import get_next_test_number, save_response, test_wagyu_sports

__all__ = ['OddsClient', 'get_next_test_number', 'save_response', 'test_wagyu_sports']
