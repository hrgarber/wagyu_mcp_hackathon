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

## Integration with MCP Clients

### Integration with Cline

To use this MCP server with Cline:

1. Add the server to Cline's MCP settings file located at:
   - macOS: `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
   - Windows: `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`

2. Add the following configuration:
   ```json
   {
     "mcpServers": {
       "wagyu-sports": {
         "command": "python",
         "args": ["/path/to/wagyu_mcp_hackathon/wagyu_sports/mcp_server/test_server.py"],
         "env": {
           "ODDS_API_KEY": "your_api_key"
         },
         "disabled": false,
         "autoApprove": []
       }
     }
   }
   ```

3. Replace `/path/to/wagyu_mcp_hackathon` with the actual path to your project
4. Replace `your_api_key` with your actual API key from [The Odds API](https://the-odds-api.com/)
5. Restart Cline

### Integration with Claude Desktop

To use this MCP server with Claude Desktop:

1. Add the server to Claude Desktop's configuration file located at:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the following configuration:
   ```json
   {
     "mcpServers": {
       "wagyu-sports": {
         "command": "python",
         "args": ["/path/to/wagyu_mcp_hackathon/wagyu_sports/mcp_server/test_server.py"],
         "env": {
           "ODDS_API_KEY": "your_api_key"
         },
         "disabled": false,
         "autoApprove": []
       }
     }
   }
   ```

3. Replace `/path/to/wagyu_mcp_hackathon` with the actual path to your project
4. Replace `your_api_key` with your actual API key from [The Odds API](https://the-odds-api.com/)
5. Restart Claude Desktop

## Test Mode

The server can be run in test mode by adding the `--test-mode` flag to the command:

```json
"args": ["/path/to/wagyu_mcp_hackathon/wagyu_sports/mcp_server/test_server.py", "--test-mode"]
```

In test mode, the server uses mock data from the `mocks_live/` directory instead of making real API calls, which:
- Doesn't require an API key
- Doesn't consume your API quota
- Works offline
