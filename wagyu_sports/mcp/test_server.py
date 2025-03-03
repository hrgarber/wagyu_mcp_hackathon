#!/usr/bin/env python3
"""
Test script for the Wagyu Sports MCP Server.

This script initializes and runs the MCP server in test mode,
which uses mock data instead of making real API calls.
"""
import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path to import from wagyu_sports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from wagyu_sports.mcp import OddsMcpServer

async def main():
    """Run the MCP server in test mode."""
    print("Starting Wagyu Sports MCP Server in test mode...")
    print("This will use mock data instead of making real API calls.")
    print()
    
    # Initialize server in test mode
    server = OddsMcpServer(test_mode=True)
    
    # Run the server
    await server.run()

if __name__ == "__main__":
    print("=" * 80)
    print("Wagyu Sports MCP Server Test")
    print("=" * 80)
    print()
    print("To test this server with mcp_inspector:")
    print("1. In another terminal, run:")
    print("   npx @modelcontextprotocol/inspector python wagyu_sports/mcp/test_server.py")
    print()
    print("2. The inspector will connect to this server and allow you to:")
    print("   - View and test available tools")
    print("   - See the results of tool calls")
    print("   - Monitor server logs")
    print()
    print("3. Try calling these tools:")
    print("   - get_sports")
    print("   - get_odds (with sport='basketball_nba')")
    print("   - get_quota_info")
    print()
    print("=" * 80)
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
