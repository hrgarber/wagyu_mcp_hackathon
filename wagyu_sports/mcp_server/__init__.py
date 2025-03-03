"""
Wagyu Sports MCP Server

This module provides an MCP server implementation for the Wagyu Sports API.
"""

try:
    # When imported as a package
    from .odds_client_server import OddsMcpServer
except ImportError:
    # When run directly
    from odds_client_server import OddsMcpServer

__all__ = ["OddsMcpServer"]
