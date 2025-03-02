#!/usr/bin/env python3
"""
Tests for the Wagyu Sports client.

This file contains all tests for the Wagyu Sports client, including:
- Unit tests for the OddsClient class
- Import verification
- Installation verification
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock
import importlib.util

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the client
from wagyu_sports import OddsClient
from dotenv import load_dotenv


def test_import():
    """Test that the OddsClient can be imported."""
    # If we got this far, the import worked
    assert OddsClient is not None
    
    # Try creating an instance
    client = OddsClient("test_key")
    assert client is not None
    assert client.api_key == "test_key"


def test_dependencies():
    """Test that required dependencies are installed."""
    dependencies = ["requests", "dotenv"]
    
    for dep in dependencies:
        spec = importlib.util.find_spec(dep)
        assert spec is not None, f"{dep} is not installed"


@pytest.fixture
def client():
    """Fixture to create an OddsClient instance."""
    return OddsClient("test_api_key")


@patch('requests.get')
def test_get_sports(mock_get, client):
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
    result = client.get_sports()
    
    # Verify the request
    mock_get.assert_called_once_with(
        'https://api.the-odds-api.com/v4/sports',
        params={'apiKey': 'test_api_key'}
    )
    
    # Verify the result
    assert result['data'] == mock_response.json.return_value
    assert result['headers']['x-requests-remaining'] == '100'
    assert result['headers']['x-requests-used'] == '5'


@patch('requests.get')
def test_get_odds(mock_get, client):
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
    result = client.get_odds("basketball_nba", options)
    
    # Verify the request
    expected_params = {'apiKey': 'test_api_key'}
    expected_params.update(options)
    mock_get.assert_called_once_with(
        'https://api.the-odds-api.com/v4/sports/basketball_nba/odds',
        params=expected_params
    )
    
    # Verify the result
    assert result['data'] == mock_response.json.return_value
    assert result['headers']['x-requests-remaining'] == '99'
    assert result['headers']['x-requests-used'] == '6'


@patch('requests.get')
def test_make_request_error(mock_get, client):
    """Test error handling in make_request method."""
    # Mock response with error
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("API Error")
    mock_get.return_value = mock_response
    
    # Call the method and expect exception
    with pytest.raises(Exception):
        client.make_request("/test")
    
    # Verify the request was made
    mock_get.assert_called_once_with(
        'https://api.the-odds-api.com/v4/test',
        params=None
    )


def test_api_key_env():
    """Test that the API key can be loaded from environment variables."""
    # Load environment variables from .env file
    load_dotenv(dotenv_path="config/.env")
    
    # Get API key
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        pytest.skip("ODDS_API_KEY not set in environment")
    
    # If we have an API key, create a client and verify it works
    # Note: This test only verifies the API key is loaded correctly,
    # it does NOT make any actual API calls
    client = OddsClient(api_key)
    assert client.api_key == api_key
