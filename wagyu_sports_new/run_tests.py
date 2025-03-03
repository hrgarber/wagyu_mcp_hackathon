#!/usr/bin/env python3
"""
Test runner for Wagyu Sports MCP server.

This script runs the tests for the Wagyu Sports MCP server.
"""
import os
import sys
import pytest


def main():
    """Run the tests."""
    print("=== Wagyu Sports MCP Server Tests ===")
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set environment variable for anyio backend
    os.environ["ANYIO_BACKEND"] = "asyncio"
    
    # Run the tests
    result = pytest.main(["-xvs", os.path.join(script_dir, "tests", "test_mcp_server.py")])
    
    # Return the exit code
    return result


if __name__ == "__main__":
    sys.exit(main())
