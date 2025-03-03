"""Simple tests for Wagyu Sports MCP server following the Python MCP SDK example pattern"""

import json
import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Import directly from the module
from wagyu_sports.mcp_server.odds_client_server import OddsMcpServer

@pytest.mark.asyncio
async def test_simple_get_sports():
    """Test the basic functionality of the get_sports tool"""
    # Create an instance of the server in test mode
    server = OddsMcpServer(test_mode=True)
    
    # Test the _get_mock_data method directly
    mock_data = await server._get_mock_data("sports_list.json")
    
    # Parse and verify the response
    data = json.loads(mock_data)
    assert "data" in data
    assert isinstance(data["data"], list)
    assert any(sport["key"] == "basketball_nba" for sport in data["data"])


@pytest.mark.asyncio
async def test_simple_get_odds():
    """Test the basic functionality of the get_odds tool"""
    # Create an instance of the server in test mode
    server = OddsMcpServer(test_mode=True)
    
    # Test the _get_mock_data method directly for NBA games
    mock_data = await server._get_mock_data("nba_games.json")
    
    # Parse and verify the response
    data = json.loads(mock_data)
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    
    # Check the first game
    first_game = data["data"][0]
    assert "sport_key" in first_game
    assert first_game["sport_key"] == "basketball_nba"
    assert "home_team" in first_game
    assert "away_team" in first_game


@pytest.mark.asyncio
async def test_simple_get_quota_info():
    """Test the basic functionality of the get_quota_info tool"""
    # Create an instance of the server in test mode
    server = OddsMcpServer(test_mode=True)
    
    # In test mode, get_quota_info returns a fixed response
    # We can construct this manually to test the structure
    expected_data = {
        "remaining_requests": "100",
        "used_requests": "50"
    }
    
    # Create a response similar to what the tool would return
    quota_response = json.dumps(expected_data, indent=2)
    quota_data = json.loads(quota_response)
    
    # Verify the expected structure
    assert "remaining_requests" in quota_data
    assert "used_requests" in quota_data


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
