# Wagyu Sports MCP Server

This directory contains a Model Context Protocol (MCP) server implementation for the Wagyu Sports API. The MCP server wraps the existing `OddsClient` and exposes its functionality through the standardized MCP interface.

## Features

- Exposes sports betting data through MCP tools
- Supports test mode with mock data for development and testing
- Compatible with any MCP client (Claude Desktop, Cline, etc.)

## Available Tools

The server exposes the following tools:

- `get_sports`: Get a list of available sports
- `get_odds`: Get odds for a specific sport
- `get_quota_info`: Get API quota information

## Usage

### Basic Usage

```python
from wagyu_sports.mcp import OddsMcpServer

# Initialize with API key
server = OddsMcpServer(api_key="your_api_key")

# Run the server
import asyncio
asyncio.run(server.run())
```

### Test Mode

The server can be run in test mode, which uses mock data instead of making real API calls:

```python
# Initialize in test mode (no API key required)
server = OddsMcpServer(test_mode=True)

# Run the server
import asyncio
asyncio.run(server.run())
```

## Testing with MCP Inspector

You can test the server using the MCP Inspector tool:

1. Run the test server:
   ```
   python wagyu_sports/mcp/test_server.py
   ```

2. In another terminal, run the MCP Inspector:
   ```
   npx @modelcontextprotocol/inspector python wagyu_sports/mcp/test_server.py
   ```

3. The inspector will connect to the server and allow you to:
   - View and test available tools
   - See the results of tool calls
   - Monitor server logs

## Integration with Cline

To use this MCP server with Cline:

1. Add the server to Cline's MCP settings:
   ```json
   {
     "mcpServers": {
       "wagyu-sports": {
         "command": "python",
         "args": ["/path/to/wagyu_mcp_hackathon/wagyu_sports/mcp/test_server.py"],
         "env": {
           "ODDS_API_KEY": "your_api_key"
         }
       }
     }
   }
   ```

2. Restart Cline

3. The tools will be available for use in Cline

## Mock Data

When running in test mode, the server uses mock data from the `mocks/` directory:

- `sports_list.json`: Sample list of available sports
- `nba_games.json`: Sample NBA game data
- `game_odds_all_books.json`: Sample odds data from multiple bookmakers

You can modify these files to test different scenarios.

## Implementation Details

The server is implemented using the Python MCP SDK and follows the MCP protocol specification. It wraps the existing `OddsClient` class and exposes its functionality through MCP tools.

The implementation includes:
- Tool registration and execution
- Test mode with mock data
- Error handling
- API quota tracking
