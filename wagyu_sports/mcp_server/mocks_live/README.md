# Live API Response Captures

This directory contains captures of live API responses from the Odds API. These captures can be used for creating updated mock data for testing.

## Using Live Mode

The MCP server has been modified to support overriding the test mode setting on a per-call basis. To use the live API (which costs money per call), set the `use_test_mode` parameter to `false` in your tool calls.

### Example Usage

```python
# Get sports list using live API
<use_mcp_tool>
<server_name>wagyu-sports</server_name>
<tool_name>get_sports</tool_name>
<arguments>
{
  "all_sports": true,
  "use_test_mode": false
}
</arguments>
</use_mcp_tool>

# Get NBA odds using live API
<use_mcp_tool>
<server_name>wagyu-sports</server_name>
<tool_name>get_odds</tool_name>
<arguments>
{
  "sport": "basketball_nba",
  "regions": "us",
  "markets": "h2h,spreads",
  "use_test_mode": false
}
</arguments>
</use_mcp_tool>

# Get quota information using live API
<use_mcp_tool>
<server_name>wagyu-sports</server_name>
<tool_name>get_quota_info</tool_name>
<arguments>
{
  "use_test_mode": false
}
</arguments>
</use_mcp_tool>
```

## Important Notes

1. **Cost Awareness**: Each live API call costs money. Use sparingly and only when necessary.
2. **Server Restart Required**: After modifying the server code, the MCP server needs to be restarted for changes to take effect.
3. **API Key**: The live mode requires a valid API key, which is already configured in the MCP settings.

## Captured Responses

The following live API responses have been captured:

- `sports_list_live.json`: List of available sports
- `nba_games_live.json`: NBA game odds data
- `quota_info_live.json`: API quota information
