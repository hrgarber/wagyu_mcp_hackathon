#!/usr/bin/env python3
"""
Wagyu Sports MCP Server Implementation

This module provides an MCP server that exposes the Wagyu Sports API
functionality through the Model Context Protocol.
"""
import os
import sys
import json
import asyncio
from typing import Dict, Any, Optional, List, Union
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

from ..odds_client import OddsClient

class OddsMcpServer:
    """MCP server for Wagyu Sports odds API."""
    
    def __init__(self, api_key: Optional[str] = None, test_mode: bool = False):
        """
        Initialize the MCP server.
        
        Args:
            api_key (str, optional): API key for the Odds API. If not provided,
                                    will try to get from environment variable.
            test_mode (bool): Whether to use mock data instead of real API calls.
        """
        # Get API key from environment if not provided
        self.api_key = api_key or os.environ.get("ODDS_API_KEY")
        if not self.api_key and not test_mode:
            raise ValueError("API key is required when not in test mode")
            
        self.test_mode = test_mode
        self.mock_data_dir = Path(__file__).parent / "mocks"
        
        # Initialize client
        self.client = OddsClient(self.api_key) if not test_mode else None
        
        # Initialize server
        self.server = Server("wagyu-sports-mcp")
        
        # Register handlers
        self._register_tools()
        
    def _register_tools(self):
        """Register MCP tools."""
        
        @self.server.tool()
        async def get_sports(all_sports: bool = False) -> str:
            """
            Get a list of available sports.
            
            Args:
                all_sports: Include out-of-season sports if True
                
            Returns:
                JSON string with sports data
            """
            if self.test_mode:
                return await self._get_mock_data("sports_list.json")
            
            result = self.client.get_sports(all_sports=all_sports)
            return json.dumps(result, indent=2)
        
        @self.server.tool()
        async def get_odds(sport: str, regions: Optional[str] = None, 
                          markets: Optional[str] = None, 
                          odds_format: Optional[str] = None,
                          date_format: Optional[str] = None) -> str:
            """
            Get odds for a specific sport.
            
            Args:
                sport: Sport key (e.g., 'basketball_nba')
                regions: Comma-separated list of regions (e.g., 'us,uk')
                markets: Comma-separated list of markets (e.g., 'h2h,spreads')
                odds_format: Format for odds ('decimal' or 'american')
                date_format: Format for dates ('unix' or 'iso')
                
            Returns:
                JSON string with odds data
            """
            if self.test_mode:
                if sport == "basketball_nba":
                    return await self._get_mock_data("nba_games.json")
                return await self._get_mock_data("game_odds_all_books.json")
            
            options = {}
            if regions:
                options["regions"] = regions
            if markets:
                options["markets"] = markets
            if odds_format:
                options["oddsFormat"] = odds_format
            if date_format:
                options["dateFormat"] = date_format
                
            result = self.client.get_odds(sport, options=options)
            return json.dumps(result, indent=2)
        
        @self.server.tool()
        async def get_quota_info() -> str:
            """
            Get API quota information.
            
            Returns:
                JSON string with quota information
            """
            if self.test_mode:
                return json.dumps({
                    "remaining_requests": "100",
                    "used_requests": "50"
                }, indent=2)
            
            return json.dumps({
                "remaining_requests": self.client.remaining_requests,
                "used_requests": self.client.used_requests
            }, indent=2)
    
    async def _get_mock_data(self, filename: str) -> str:
        """
        Get mock data from a JSON file.
        
        Args:
            filename: Name of the mock data file
            
        Returns:
            JSON string with mock data
        """
        try:
            mock_file = self.mock_data_dir / filename
            if not mock_file.exists():
                return json.dumps({"error": f"Mock file {filename} not found"})
                
            with open(mock_file, "r") as f:
                data = json.load(f)
                
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Error loading mock data: {str(e)}"})
    
    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as streams:
            await self.server.run(
                streams[0],
                streams[1],
                self.server.create_initialization_options()
            )
            
def main():
    """Run the MCP server as a standalone process."""
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser(description="Wagyu Sports MCP Server")
    parser.add_argument("--api-key", help="API key for the Odds API")
    parser.add_argument("--test-mode", action="store_true", help="Use mock data instead of real API calls")
    args = parser.parse_args()
    
    # Create and run server
    server = OddsMcpServer(api_key=args.api_key, test_mode=args.test_mode)
    asyncio.run(server.run())

if __name__ == "__main__":
    main()
