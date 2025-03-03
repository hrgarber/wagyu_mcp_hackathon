"""Tests for Wagyu Sports MCP server"""

import os
import sys
import pytest
import json

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from mcp.shared.memory import (
    create_connected_server_and_client_session as client_session,
)
from mcp.types import TextContent, TextResourceContents

from wagyu_sports.mcp_server.odds_client_server import OddsMcpServer


@pytest.mark.anyio
async def test_get_sports():
    """Test the get_sports tool"""
    server = OddsMcpServer(test_mode=True)
    
    async with client_session(server.server) as client:
        result = await client.call_tool("get_sports", {})
        assert len(result.content) == 1
        content = result.content[0]
        assert isinstance(content, TextContent)
        
        # Parse the JSON response
        response_data = json.loads(content.text)
        
        # Check that the response contains expected data
        assert "data" in response_data
        assert isinstance(response_data["data"], list)
        
        # Check for a specific sport (basketball_nba should be in the mock data)
        basketball_nba = next((s for s in response_data["data"] if s["key"] == "basketball_nba"), None)
        assert basketball_nba is not None
        assert basketball_nba["title"] == "NBA"


@pytest.mark.anyio
async def test_get_odds():
    """Test the get_odds tool"""
    server = OddsMcpServer(test_mode=True)
    
    async with client_session(server.server) as client:
        result = await client.call_tool("get_odds", {"sport": "basketball_nba"})
        assert len(result.content) == 1
        content = result.content[0]
        assert isinstance(content, TextContent)
        
        # Parse the JSON response
        response_data = json.loads(content.text)
        
        # Check that the response contains expected data
        assert "data" in response_data
        assert isinstance(response_data["data"], list)
        
        # Check that at least one game is returned
        assert len(response_data["data"]) > 0
        
        # Check that the first game has the expected fields
        first_game = response_data["data"][0]
        assert "sport_key" in first_game
        assert first_game["sport_key"] == "basketball_nba"
        assert "home_team" in first_game
        assert "away_team" in first_game
        assert "bookmakers" in first_game


@pytest.mark.anyio
async def test_get_odds_with_options():
    """Test the get_odds tool with options"""
    server = OddsMcpServer(test_mode=True)
    
    async with client_session(server.server) as client:
        result = await client.call_tool(
            "get_odds", 
            {
                "sport": "soccer_epl",
                "regions": "us",
                "markets": "h2h,spreads",
                "odds_format": "american",
                "date_format": "iso"
            }
        )
        assert len(result.content) == 1
        content = result.content[0]
        assert isinstance(content, TextContent)
        
        # Parse the JSON response
        response_data = json.loads(content.text)
        
        # Check that the response contains expected data
        assert "data" in response_data
        assert isinstance(response_data["data"], list)
        
        # Check that at least one game is returned
        assert len(response_data["data"]) > 0
        
        # Check that the first game has the expected fields
        first_game = response_data["data"][0]
        assert "sport_key" in first_game
        assert first_game["sport_key"] == "soccer_epl"


@pytest.mark.anyio
async def test_get_quota_info():
    """Test the get_quota_info tool"""
    server = OddsMcpServer(test_mode=True)
    
    async with client_session(server.server) as client:
        result = await client.call_tool("get_quota_info", {})
        assert len(result.content) == 1
        content = result.content[0]
        assert isinstance(content, TextContent)
        
        # Parse the JSON response
        response_data = json.loads(content.text)
        
        # Check that the response contains expected fields
        assert "remaining_requests" in response_data
        assert "used_requests" in response_data


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
