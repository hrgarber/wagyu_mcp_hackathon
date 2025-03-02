"""
Tool Testing Package for Enhanced Odds API Client

This package contains enhanced versions of the Odds API client with
additional function calling capabilities for more dynamic queries.
"""

from .enhanced_client import EnhancedOddsClient
from .query_engine import OddsQueryEngine

__all__ = ['EnhancedOddsClient', 'OddsQueryEngine']
