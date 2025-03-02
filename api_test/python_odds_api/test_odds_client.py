#!/usr/bin/env python3
"""
Unit tests for the OddsClient class.
"""
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_odds_api import OddsClient


class TestOddsClient(unittest.TestCase):
    """Test cases for the OddsClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Load environment variables
        load_dotenv()
        
        # Get API key or use a dummy key for tests
        self.api_key = os.getenv("ODDS_API_KEY", "test_api_key")
        
        # Create client
        self.client = OddsClient(self.api_key)
    
    @patch('requests.get')
    def test_get_sports(self, mock_get):
        """Test the get_sports method."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"key": "sport1", "title": "Sport 1"},
            {"key": "sport2", "title": "Sport 2"}
        ]
        mock_response.headers = {
            'x-requests-remaining': '100',
            'x-requests-used': '5'
        }
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.get_sports()
        
        # Verify the request
        mock_get.assert_called_once_with(
            'https://api.the-odds-api.com/v4/sports',
            params={'apiKey': self.api_key}
        )
        
        # Verify the result
        self.assertEqual(result['data'], mock_response.json.return_value)
        self.assertEqual(result['headers']['x-requests-remaining'], '100')
        self.assertEqual(result['headers']['x-requests-used'], '5')
    
    @patch('requests.get')
    def test_get_odds(self, mock_get):
        """Test the get_odds method."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "id": "game1",
                "home_team": "Team A",
                "away_team": "Team B",
                "bookmakers": []
            }
        ]
        mock_response.headers = {
            'x-requests-remaining': '99',
            'x-requests-used': '6'
        }
        mock_get.return_value = mock_response
        
        # Options for the request
        options = {
            "regions": "us",
            "markets": "h2h",
            "oddsFormat": "decimal"
        }
        
        # Call the method
        result = self.client.get_odds("basketball_nba", options)
        
        # Verify the request
        expected_params = {'apiKey': self.api_key}
        expected_params.update(options)
        mock_get.assert_called_once_with(
            'https://api.the-odds-api.com/v4/sports/basketball_nba/odds',
            params=expected_params
        )
        
        # Verify the result
        self.assertEqual(result['data'], mock_response.json.return_value)
        self.assertEqual(result['headers']['x-requests-remaining'], '99')
        self.assertEqual(result['headers']['x-requests-used'], '6')
    
    @patch('requests.get')
    def test_make_request_error(self, mock_get):
        """Test error handling in make_request method."""
        # Mock response with error
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response
        
        # Call the method and expect exception
        with self.assertRaises(Exception):
            self.client.make_request("/test")
        
        # Verify the request was made
        mock_get.assert_called_once_with(
            'https://api.the-odds-api.com/v4/test',
            params=None
        )


if __name__ == '__main__':
    unittest.main()
