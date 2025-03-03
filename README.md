# Wagyu Sports MCP Server

A Model Context Protocol (MCP) server for sports betting data, providing access to The Odds API through Claude and other MCP-compatible AI assistants.

```mermaid
graph LR
    Claude([Claude]) --> MCP[Wagyu Sports MCP]
    MCP --> API[The Odds API]
    API --> MCP --> Claude
    
    style Claude fill:#f8f8f8,stroke:#666,stroke-width:1px,color:#000
    style MCP fill:#34A853,stroke:#1E8E3E,stroke-width:2px,color:#fff
    style API fill:#F5F5F5,stroke:#999,stroke-width:1px,color:#000
```

## Quick Setup

1. **Install the package**:
   ```bash
   uvx install wagyu_sports
   ```

2. **Add to your MCP configuration**:

   For Cline, add to `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`:

   ```json
   {
     "mcpServers": {
       "wagyu-sports": {
         "command": "uvx",
         "args": ["run", "wagyu_sports.mcp_server.test_server", "--test-mode"],
         "env": {
           "ODDS_API_KEY": "your_api_key_here"
         },
         "disabled": false,
         "autoApprove": []
       }
     }
   }
   ```

   For Claude Desktop, add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

   ```json
   {
     "mcpServers": {
       "wagyu-sports": {
         "command": "uvx",
         "args": ["run", "wagyu_sports.mcp_server.test_server", "--test-mode"],
         "env": {
           "ODDS_API_KEY": "your_api_key_here"
         },
         "disabled": false,
         "autoApprove": []
       }
     }
   }
   ```

3. **Get an API key** from [The Odds API](https://the-odds-api.com/) and replace `your_api_key_here` in the configuration.

4. **Restart your MCP client** (Cline or Claude Desktop).

## Available Tools

The MCP server provides the following tools:

- `get_sports`: Get a list of available sports
- `get_odds`: Get odds for a specific sport
- `get_quota_info`: Get API quota information

## Test Mode vs. Real Mode

### Test Mode (Recommended for Getting Started)

Test mode uses mock data instead of making real API calls. This is useful for:
- Development and testing without API rate limits
- Demos and presentations
- Learning how to use the MCP server

To use test mode:
1. Set `--test-mode` in your MCP configuration (as shown in the Quick Setup)
2. No API key is required
3. The server will return consistent mock data for all requests

Example configuration for test mode:
```json
"args": ["run", "wagyu_sports.mcp_server.test_server", "--test-mode"]
```

### Real Mode (For Production Use)

Real mode makes actual API calls to The Odds API. This is necessary for:
- Getting real-time sports betting data
- Production applications
- Accurate odds information

To use real mode:
1. Remove the `--test-mode` flag from your MCP configuration
2. Provide a valid API key from The Odds API
3. Be aware of API rate limits (typically 500 requests per month for free tier)

Example configuration for real mode:
```json
"args": ["run", "wagyu_sports.mcp_server.test_server"],
"env": {
  "ODDS_API_KEY": "your_actual_api_key_here"
}
```

You can also run the server directly with:
```bash
uvx run wagyu_sports.mcp_server.test_server --api-key=your_api_key_here
```

## Development

For development and testing:

```bash
# Clone the repository
git clone https://github.com/your-username/wagyu_mcp_hackathon.git
cd wagyu_mcp_hackathon

# Install in development mode
uvx install -e .

# Run tests
uvx run pytest wagyu_sports/tests
```

## Project Structure

- `wagyu_sports/mcp_server/` - MCP server implementation
- `wagyu_sports/tests/` - Test files
- `wagyu_sports/examples/` - Example scripts

## For More Information

See the `wagyu_sports/README.md` file for details on using the Python client directly.
