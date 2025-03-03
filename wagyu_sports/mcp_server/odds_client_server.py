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

from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server
import mcp.types as types

try:
    # When imported as a package
    from .odds_client import OddsClient
except ImportError:
    # When run directly
    from odds_client import OddsClient

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
        self.mock_data_dir = Path(__file__).parent / "mocks_live"
        
        # Initialize client
        self.client = OddsClient(self.api_key) if not test_mode else None
        
        # Initialize server with FastMCP
        self.server = FastMCP("wagyu-sports-mcp")
        
        # Register tools
        self.register_tools()
    
    def register_tools(self):
        """Register MCP tools."""
        
        @self.server.tool()
        async def get_sports(all_sports: bool = False, use_test_mode: Optional[bool] = None) -> str:
            """
            Get a list of available sports.
            
            Args:
                all_sports: Include out-of-season sports if True
                use_test_mode: Override server test_mode setting (True for mock data, False for real API)
                
            Returns:
                JSON string with sports data
            """
            # Determine if we should use test mode
            test_mode = use_test_mode if use_test_mode is not None else self.test_mode
            
            if test_mode:
                return await self._get_mock_data("sports_list_live.json")
            
            result = self.client.get_sports(all_sports=all_sports)
            return json.dumps(result, indent=2)
        
        @self.server.tool()
        async def get_odds(sport: str, regions: Optional[str] = None, 
                          markets: Optional[str] = None, 
                          odds_format: Optional[str] = None,
                          date_format: Optional[str] = None,
                          use_test_mode: Optional[bool] = None) -> str:
            """
            Get odds for a specific sport.
            
            Args:
                sport: Sport key (e.g., 'basketball_nba')
                regions: Comma-separated list of regions (e.g., 'us,uk')
                markets: Comma-separated list of markets (e.g., 'h2h,spreads')
                odds_format: Format for odds ('decimal' or 'american')
                date_format: Format for dates ('unix' or 'iso')
                use_test_mode: Override server test_mode setting (True for mock data, False for real API)
                
            Returns:
                JSON string with odds data
            """
            # Determine if we should use test mode
            test_mode = use_test_mode if use_test_mode is not None else self.test_mode
            
            if test_mode:
                if sport == "basketball_nba":
                    return await self._get_mock_data("nba_games_live.json")
                # Fall back to nba_games_live.json since we don't have a live version of game_odds_all_books.json
                return await self._get_mock_data("nba_games_live.json")
            
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
        async def get_quota_info(use_test_mode: Optional[bool] = None) -> str:
            """
            Get API quota information.
            
            Args:
                use_test_mode: Override server test_mode setting (True for mock data, False for real API)
                
            Returns:
                JSON string with quota information
            """
            # Determine if we should use test mode
            test_mode = use_test_mode if use_test_mode is not None else self.test_mode
            
            if test_mode:
                return await self._get_mock_data("quota_info_live.json")
            
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
        # FastMCP has a different API for running the server
        # We need to use the run_stdio_async method directly
        await self.server.run_stdio_async()
            
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
