# Wagyu Sports MCP Server Implementation Plan

This document outlines the plan for implementing a Model Context Protocol (MCP) server for Wagyu Sports. The MCP server will expose the Wagyu Sports API client as a set of tools and resources that can be used by AI models.

## Overview

The MCP server will provide:

1. **Tools**: Methods for fetching sports data, odds, and scores
2. **Resources**: Access to archived API responses

## Prerequisites

Before implementing the MCP server, we need to:

1. Complete the Wagyu Sports enhancement project
2. Set up the response archive with a good set of sample data
3. Ensure the API client is stable and well-tested

## Directory Structure

```
wagyu_sports/
├── __init__.py
├── odds_client.py
├── utils.py
├── responses/
├── validators/
├── endpoints/
└── mcp/
    ├── __init__.py
    ├── server.py        # MCP server implementation
    ├── tools.py         # Tool implementations
    └── resources.py     # Resource implementations
```

## MCP Server Implementation

The MCP server will be implemented using the MCP SDK:

```python
#!/usr/bin/env python3
import os
import sys
from typing import Dict, Any, Optional

from modelcontextprotocol.sdk.server import Server
from modelcontextprotocol.sdk.server.stdio import StdioServerTransport
from modelcontextprotocol.sdk.types import (
    CallToolRequestSchema,
    ErrorCode,
    ListResourcesRequestSchema,
    ListResourceTemplatesRequestSchema,
    ListToolsRequestSchema,
    McpError,
    ReadResourceRequestSchema,
)

from wagyu_sports import OddsClient
from wagyu_sports.mcp.tools import WagyuSportsTools
from wagyu_sports.mcp.resources import WagyuSportsResources

class WagyuSportsMcpServer:
    """MCP server for Wagyu Sports."""
    
    def __init__(self):
        """Initialize the MCP server."""
        # Get API key from environment
        api_key = os.environ.get("ODDS_API_KEY")
        if not api_key:
            raise ValueError("ODDS_API_KEY environment variable is required")
            
        # Initialize client
        self.client = OddsClient(
            api_key=api_key,
            use_archive=True,
            mock_mode=True,  # Use mock mode to avoid consuming API credits
            debug_mode=False
        )
        
        # Initialize server
        self.server = Server(
            {
                "name": "wagyu-sports-mcp",
                "version": "0.1.0",
            },
            {
                "capabilities": {
                    "resources": {},
                    "tools": {},
                },
            }
        )
        
        # Initialize tools and resources
        self.tools = WagyuSportsTools(self.client)
        self.resources = WagyuSportsResources(self.client)
        
        # Set up request handlers
        self.setup_request_handlers()
        
        # Error handling
        self.server.onerror = lambda error: print(f"[MCP Error] {error}", file=sys.stderr)
        
    def setup_request_handlers(self):
        """Set up request handlers for the MCP server."""
        # List tools
        self.server.setRequestHandler(ListToolsRequestSchema, self.tools.list_tools)
        
        # Call tool
        self.server.setRequestHandler(CallToolRequestSchema, self.tools.call_tool)
        
        # List resources
        self.server.setRequestHandler(ListResourcesRequestSchema, self.resources.list_resources)
        
        # List resource templates
        self.server.setRequestHandler(ListResourceTemplatesRequestSchema, self.resources.list_resource_templates)
        
        # Read resource
        self.server.setRequestHandler(ReadResourceRequestSchema, self.resources.read_resource)
        
    async def run(self):
        """Run the MCP server."""
        transport = StdioServerTransport()
        await self.server.connect(transport)
        print("Wagyu Sports MCP server running on stdio", file=sys.stderr)
        
if __name__ == "__main__":
    import asyncio
    
    server = WagyuSportsMcpServer()
    asyncio.run(server.run())
```

## Tool Implementations

The tools will be implemented in `tools.py`:

```python
from typing import Dict, Any, Optional, List

from modelcontextprotocol.sdk.types import (
    ErrorCode,
    McpError,
)

class WagyuSportsTools:
    """Tool implementations for Wagyu Sports MCP server."""
    
    def __init__(self, client):
        """
        Initialize the tools.
        
        Args:
            client: OddsClient instance
        """
        self.client = client
        
    async def list_tools(self, request):
        """List available tools."""
        return {
            "tools": [
                {
                    "name": "get_sports",
                    "description": "Get a list of available sports",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "all_sports": {
                                "type": "boolean",
                                "description": "Include out-of-season sports"
                            }
                        }
                    }
                },
                {
                    "name": "get_odds",
                    "description": "Get odds for a specific sport",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "sport": {
                                "type": "string",
                                "description": "Sport key (e.g., 'basketball_nba')"
                            },
                            "regions": {
                                "type": "string",
                                "description": "Comma-separated list of regions (e.g., 'us,uk')"
                            },
                            "markets": {
                                "type": "string",
                                "description": "Comma-separated list of markets (e.g., 'h2h,spreads')"
                            }
                        },
                        "required": ["sport"]
                    }
                },
                {
                    "name": "follow_event",
                    "description": "Get comprehensive data for a single event",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "sport": {
                                "type": "string",
                                "description": "Sport key (e.g., 'basketball_nba')"
                            },
                            "event_id": {
                                "type": "string",
                                "description": "Event ID"
                            }
                        },
                        "required": ["sport", "event_id"]
                    }
                }
            ]
        }
        
    async def call_tool(self, request):
        """Call a tool."""
        tool_name = request.params.name
        arguments = request.params.arguments
        
        try:
            if tool_name == "get_sports":
                return await self._get_sports(arguments)
            elif tool_name == "get_odds":
                return await self._get_odds(arguments)
            elif tool_name == "follow_event":
                return await self._follow_event(arguments)
            else:
                raise McpError(ErrorCode.MethodNotFound, f"Unknown tool: {tool_name}")
        except Exception as e:
            raise McpError(ErrorCode.InternalError, str(e))
            
    async def _get_sports(self, arguments):
        """Get a list of available sports."""
        all_sports = arguments.get("all_sports", False)
        
        try:
            response = self.client.get_sports(all_sports=all_sports)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Found {len(response['data'])} sports"
                    },
                    {
                        "type": "json",
                        "json": response["data"]
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error getting sports: {str(e)}"
                    }
                ],
                "isError": True
            }
            
    async def _get_odds(self, arguments):
        """Get odds for a specific sport."""
        sport = arguments.get("sport")
        if not sport:
            raise McpError(ErrorCode.InvalidParams, "Sport is required")
            
        options = {}
        if "regions" in arguments:
            options["regions"] = arguments["regions"]
        if "markets" in arguments:
            options["markets"] = arguments["markets"]
            
        try:
            response = self.client.get_odds(sport, options)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Found odds for {len(response['data'])} events"
                    },
                    {
                        "type": "json",
                        "json": response["data"]
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error getting odds: {str(e)}"
                    }
                ],
                "isError": True
            }
            
    async def _follow_event(self, arguments):
        """Get comprehensive data for a single event."""
        sport = arguments.get("sport")
        event_id = arguments.get("event_id")
        
        if not sport:
            raise McpError(ErrorCode.InvalidParams, "Sport is required")
        if not event_id:
            raise McpError(ErrorCode.InvalidParams, "Event ID is required")
            
        try:
            response = self.client.follow_event(sport, event_id)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Event details for {event_id}"
                    },
                    {
                        "type": "json",
                        "json": response
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error following event: {str(e)}"
                    }
                ],
                "isError": True
            }
```

## Resource Implementations

The resources will be implemented in `resources.py`:

```python
import os
import json
from typing import Dict, Any, Optional, List

from modelcontextprotocol.sdk.types import (
    ErrorCode,
    McpError,
)

class WagyuSportsResources:
    """Resource implementations for Wagyu Sports MCP server."""
    
    def __init__(self, client):
        """
        Initialize the resources.
        
        Args:
            client: OddsClient instance
        """
        self.client = client
        
    async def list_resources(self, request):
        """List available resources."""
        # Get a list of archived responses
        resources = []
        
        # Add a resource for each sport
        sports_response = self.client.get_sports()
        for sport in sports_response["data"]:
            resources.append({
                "uri": f"wagyu://sports/{sport['key']}",
                "name": f"Sport: {sport['title']}",
                "mimeType": "application/json",
                "description": f"Information about {sport['title']}"
            })
            
        return {"resources": resources}
        
    async def list_resource_templates(self, request):
        """List available resource templates."""
        return {
            "resourceTemplates": [
                {
                    "uriTemplate": "wagyu://sports/{sport_key}",
                    "name": "Sport information",
                    "mimeType": "application/json",
                    "description": "Information about a specific sport"
                },
                {
                    "uriTemplate": "wagyu://odds/{sport_key}",
                    "name": "Odds for a sport",
                    "mimeType": "application/json",
                    "description": "Odds for a specific sport"
                },
                {
                    "uriTemplate": "wagyu://events/{sport_key}/{event_id}",
                    "name": "Event details",
                    "mimeType": "application/json",
                    "description": "Details for a specific event"
                }
            ]
        }
        
    async def read_resource(self, request):
        """Read a resource."""
        uri = request.params.uri
        
        # Parse the URI
        if uri.startswith("wagyu://sports/"):
            sport_key = uri.replace("wagyu://sports/", "")
            return await self._get_sport(sport_key)
        elif uri.startswith("wagyu://odds/"):
            sport_key = uri.replace("wagyu://odds/", "")
            return await self._get_odds(sport_key)
        elif uri.startswith("wagyu://events/"):
            parts = uri.replace("wagyu://events/", "").split("/")
            if len(parts) != 2:
                raise McpError(ErrorCode.InvalidRequest, "Invalid event URI format")
            sport_key, event_id = parts
            return await self._get_event(sport_key, event_id)
        else:
            raise McpError(ErrorCode.InvalidRequest, f"Invalid URI format: {uri}")
            
    async def _get_sport(self, sport_key):
        """Get information about a specific sport."""
        try:
            response = self.client.get_sports()
            
            # Find the sport in the response
            sport = None
            for s in response["data"]:
                if s["key"] == sport_key:
                    sport = s
                    break
                    
            if not sport:
                raise McpError(ErrorCode.NotFound, f"Sport not found: {sport_key}")
                
            return {
                "contents": [
                    {
                        "uri": f"wagyu://sports/{sport_key}",
                        "mimeType": "application/json",
                        "text": json.dumps(sport, indent=2)
                    }
                ]
            }
        except Exception as e:
            raise McpError(ErrorCode.InternalError, str(e))
            
    async def _get_odds(self, sport_key):
        """Get odds for a specific sport."""
        try:
            response = self.client.get_odds(sport_key)
            
            return {
                "contents": [
                    {
                        "uri": f"wagyu://odds/{sport_key}",
                        "mimeType": "application/json",
                        "text": json.dumps(response["data"], indent=2)
                    }
                ]
            }
        except Exception as e:
            raise McpError(ErrorCode.InternalError, str(e))
            
    async def _get_event(self, sport_key, event_id):
        """Get details for a specific event."""
        try:
            response = self.client.follow_event(sport_key, event_id)
            
            return {
                "contents": [
                    {
                        "uri": f"wagyu://events/{sport_key}/{event_id}",
                        "mimeType": "application/json",
                        "text": json.dumps(response, indent=2)
                    }
                ]
            }
        except Exception as e:
            raise McpError(ErrorCode.InternalError, str(e))
```

## Installation and Usage

To install and use the MCP server:

1. Install the MCP SDK:
   ```bash
   pip install modelcontextprotocol-sdk
   ```

2. Set up the environment:
   ```bash
   export ODDS_API_KEY=your_api_key
   ```

3. Run the server:
   ```bash
   python -m wagyu_sports.mcp.server
   ```

4. Configure the MCP client to connect to the server.

## Benefits

The MCP server will provide several benefits:

1. **AI Integration**: Allow AI models to access sports betting data
2. **Credit Efficiency**: Use the response archive to minimize API credit usage
3. **Structured Data**: Provide structured data in a format that's easy for AI models to use
4. **Simplified Access**: Provide a simplified interface to the API

## Next Steps

1. Complete the Wagyu Sports enhancement project
2. Set up the response archive with a good set of sample data
3. Implement the MCP server
4. Test the MCP server with AI models
5. Document the MCP server and its usage
