#!/usr/bin/env python3
"""
Test script for the Wagyu Sports MCP Server.

This script initializes and runs the MCP server in test mode,
which uses mock data instead of making real API calls.
"""
import asyncio
import os
import sys
import argparse
from pathlib import Path

# Import directly from the current directory
from odds_client_server import OddsMcpServer

async def main():
    """Run the MCP server."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Wagyu Sports MCP Server")
    parser.add_argument("--test-mode", action="store_true", help="Use mock data instead of real API calls")
    args = parser.parse_args()
    
    # Determine if we should use test mode
    test_mode = args.test_mode
    
    if test_mode:
        print("Starting Wagyu Sports MCP Server in test mode...")
        print("This will use mock data instead of making real API calls.")
    else:
        print("Starting Wagyu Sports MCP Server in live mode...")
        print("This will make real API calls that cost money.")
    print()
    
    # Initialize server
    server = OddsMcpServer(test_mode=test_mode)
    
    # Run the server
    await server.run()

if __name__ == "__main__":
    print("=" * 80)
    print("Wagyu Sports MCP Server Test")
    print("=" * 80)
    print()
    print("To test this server with mcp_inspector:")
    print("1. In another terminal, run:")
    print("   npx @modelcontextprotocol/inspector python wagyu_sports/mcp_server/test_server.py")
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
