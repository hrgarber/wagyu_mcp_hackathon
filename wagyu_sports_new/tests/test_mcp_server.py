"""
Tests for the Wagyu Sports MCP server.
"""
import json
import pytest
from modelcontextprotocol.sdk.shared.memory import (
    create_connected_server_and_client_session as client_session,
)
from modelcontextprotocol.sdk.types import TextContent, TextResourceContents

from wagyu_sports_new.mcp import WagyuSportsMcpServer


@pytest.mark.anyio
async def test_list_tools():
    """Test that the server lists the expected tools."""
    server = WagyuSportsMcpServer(test_mode=True)
    
    async with client_session(server.server) as client:
        tools = await client.list_tools()
        
        # Check that the expected tools are present
        tool_names = [tool.name for tool in tools]
        assert "get_sports" in tool_names
        assert "get_odds" in tool_names
        assert "get_quota_info" in tool_names


@pytest.mark.anyio
async def test_get_sports_tool():
    """Test the get_sports tool."""
    server = WagyuSportsMcpServer(test_mode=True)
    
    async with client_session(server.server) as client:
        result = await client.call_tool("get_sports", {})
        
        # Check that the response contains content
        assert len(result.content) > 0
        assert isinstance(result.content[0], TextContent)
        
        # Parse the JSON response
        response_text = result.content[0].text
        response_data = json.loads(response_text)
        
        # Check that the response contains expected data
        assert "data" in response_data
        assert isinstance(response_data["data"], list)
        
        # Check that at least one sport is returned
        assert len(response_data["data"]) > 0
        
        # Check that the first sport has the expected fields
        first_sport = response_data["data"][0]
        assert "key" in first_sport
        assert "title" in first_sport
        assert "group" in first_sport
        
        # Check for a specific sport (basketball_nba should be in the mock data)
        basketball_nba = next((s for s in response_data["data"] if s["key"] == "basketball_nba"), None)
        assert basketball_nba is not None
        assert basketball_nba["title"] == "NBA"


@pytest.mark.anyio
async def test_get_odds_tool():
    """Test the get_odds tool."""
    server = WagyuSportsMcpServer(test_mode=True)
    
    async with client_session(server.server) as client:
        result = await client.call_tool("get_odds", {"sport": "basketball_nba"})
        
        # Check that the response contains content
        assert len(result.content) > 0
        assert isinstance(result.content[0], TextContent)
        
        # Parse the JSON response
        response_text = result.content[0].text
        response_data = json.loads(response_text)
        
        # Check that the response contains expected data
        assert "data" in response_data
        assert isinstance(response_data["data"], list)
        
        # Check that at least one game is returned
        assert len(response_data["data"]) > 0


@pytest.mark.anyio
async def test_get_quota_info_tool():
    """Test the get_quota_info tool."""
    server = WagyuSportsMcpServer(test_mode=True)
    
    async with client_session(server.server) as client:
        result = await client.call_tool("get_quota_info", {})
        
        # Check that the response contains content
        assert len(result.content) > 0
        assert isinstance(result.content[0], TextContent)
        
        # Parse the JSON response
        response_text = result.content[0].text
        response_data = json.loads(response_text)
        
        # Check that the response contains expected fields
        assert "remaining_requests" in response_data
        assert "used_requests" in response_data


@pytest.mark.anyio
async def test_list_resources():
    """Test that the server lists the expected resources."""
    server = WagyuSportsMcpServer(test_mode=True)
    
    async with client_session(server.server) as client:
        resources = await client.list_resources()
        
        # Check that at least one resource is returned
        assert len(resources) > 0
        
        # Check that the wagyu://sports resource is present
        sports_resource = next((r for r in resources if r.uri == "wagyu://sports"), None)
        assert sports_resource is not None


@pytest.mark.anyio
async def test_read_sports_resource():
    """Test reading the wagyu://sports resource."""
    server = WagyuSportsMcpServer(test_mode=True)
    
    async with client_session(server.server) as client:
        result = await client.read_resource("wagyu://sports")
        
        # Check that the response contains expected data
        assert len(result.contents) > 0
        assert result.contents[0].uri == "wagyu://sports"
        assert result.contents[0].mimeType == "application/json"
        assert isinstance(result.contents[0], TextResourceContents)
        
        # Parse the JSON response
        response_data = json.loads(result.contents[0].text)
        
        # Check that at least one sport is returned
        assert isinstance(response_data, list)
        assert len(response_data) > 0
        
        # Check that the first sport has the expected fields
        first_sport = response_data[0]
        assert "key" in first_sport
        assert "title" in first_sport
        assert "group" in first_sport
        
        # Check for a specific sport (basketball_nba should be in the mock data)
        basketball_nba = next((s for s in response_data if s["key"] == "basketball_nba"), None)
        assert basketball_nba is not None
        assert basketball_nba["title"] == "NBA"


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
