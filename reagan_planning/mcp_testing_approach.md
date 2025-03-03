# MCP Testing Approach: Mock Response System

## Overview

This document outlines a testing approach for sports betting MCPs that uses mock data instead of live API calls. This method allows for consistent, repeatable testing without API rate limits or dependencies on current sporting events.

## Core Concept

Create a layered MCP architecture with a base "Odds MCP" that other specialized MCPs can use. This base MCP can operate in either live mode (real API calls) or test mode (predetermined mock responses).

## Implementation Steps

### 1. Create Mock Data Files

```
/mocks/
  sports_list.json         # Available sports
  nba_games.json           # List of NBA games
  game_odds_caesars.json   # Single game odds from default book
  game_odds_all_books.json # Comparison across books
  futures_odds.json        # Championship futures odds
```

### 2. Build a Test-Ready Base MCP

```python
# Base MCP with test/live mode toggle
class OddsMCP:
    def __init__(self, api_key=None, test_mode=False):
        self.api_key = api_key
        self.test_mode = test_mode
        
    def get_data(self, endpoint, params=None):
        if self.test_mode:
            # Return appropriate mock based on endpoint and params
            return self._get_mock_response(endpoint, params)
        else:
            # Make actual API call
            return self._call_api(endpoint, params)
```

### 3. Create Specialized MCPs Using the Base

```python
# Example of a specialized MCP
class GameBrowserMCP:
    def __init__(self, odds_mcp):
        self.odds_mcp = odds_mcp
        
    def get_available_sports(self):
        # Uses the base MCP, which could be in test mode
        return self.odds_mcp.get_data("sports")
        
    def get_games_for_sport(self, sport):
        return self.odds_mcp.get_data("games", {"sport": sport})
```

## Benefits

1. **Controlled Testing Environment**: Predictable data for each test scenario
2. **Fast Execution**: No network delays or API rate limits
3. **Comprehensive Coverage**: Test edge cases and rare situations
4. **Isolated Components**: Test each MCP layer independently
5. **Repeatable Results**: Tests produce consistent output

## Mock Data Example

```json
// Example mock for a game odds response
{
  "game": {
    "home_team": "Lakers",
    "away_team": "Grizzlies",
    "commence_time": "2025-03-02T19:30:00Z"
  },
  "odds": {
    "caesars": {
      "spread": {"home": -4.5, "away": 4.5, "odds": -110},
      "moneyline": {"home": -190, "away": 160},
      "totals": {"over": 224.5, "under": 224.5, "odds": -110}
    }
  }
}
```

## Test Flow

1. Initialize test versions of MCPs with `test_mode=True`
2. Run through user scenarios from the test_scenarios.md document
3. Compare MCP outputs to expected responses
4. Toggle to live mode for final verification with real data

This approach provides a stable foundation for development while keeping the option to test against live data when needed.
