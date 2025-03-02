# Enhanced Odds API Client

This package extends the base Odds API client with additional function calling capabilities for more dynamic and specific queries.

## Features

Currently implemented:

- `get_available_sports_tonight(region="us", start_time=None, end_time=None, timezone_str=None)`: Get sports that have games available for betting between the specified times in the specified region.
  - `region`: Region to check for betting availability (e.g., "us", "uk", "eu")
  - `start_time`: Optional custom start time for filtering games (defaults to current time)
  - `end_time`: Optional custom end time for filtering games (defaults to 11:59 PM local time)
  - `timezone_str`: Optional timezone string (e.g., "America/Los_Angeles", "America/New_York") for time calculations (defaults to America/Los_Angeles)

## Usage

```python
import os
import pytz
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from api_test.tool_testing import EnhancedOddsClient

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("ODDS_API_KEY")

# Create enhanced client
client = EnhancedOddsClient(api_key)

# Example 1: Get sports available tonight in the US region (Pacific Time)
tonight_sports = client.get_available_sports_tonight(
    region="us",
    timezone_str="America/Los_Angeles"  # Pacific Time
)

# Print results
print(f"Found {len(tonight_sports['data'])} sports with games tonight (Pacific Time):")
for sport in tonight_sports['data']:
    print(f"- {sport['title']}: {sport['games_count']} games")

# Example 2: Get sports available tonight in Eastern Time
et_sports = client.get_available_sports_tonight(
    region="us",
    timezone_str="America/New_York"  # Eastern Time
)

# Print results
print(f"Found {len(et_sports['data'])} sports with games tonight (Eastern Time):")
for sport in et_sports['data']:
    print(f"- {sport['title']}: {sport['games_count']} games")

# Example 3: Get sports with games in the next 3 hours in local timezone
now_local = datetime.now(pytz.timezone('America/Los_Angeles'))
end_time_local = now_local + timedelta(hours=3)

next_3_hours_sports = client.get_available_sports_tonight(
    region="us",
    start_time=now_local,
    end_time=end_time_local
)

# Print results
print(f"Found {len(next_3_hours_sports['data'])} sports with games in the next 3 hours:")
for sport in next_3_hours_sports['data']:
    print(f"- {sport['title']}: {sport['games_count']} games")

# Example 4: Access local time information for games
if next_3_hours_sports['data'] and next_3_hours_sports['data'][0].get('sample_game'):
    game = next_3_hours_sports['data'][0]['sample_game']
    if 'commence_time_local' in game:
        local_time = datetime.fromisoformat(game['commence_time_local'])
        print(f"Game starts at: {local_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
```

## Example

Run the example script to see the enhanced client in action:

```bash
python api_test/tool_testing/example.py
```

This will display all sports with games available for betting tonight in the US region, along with a sample game and odds for each sport.

## Future Enhancements

Planned future enhancements include:

1. `get_matchup_odds(sport, team_name)`: Get odds for a specific team's matchups.
2. `filter_games_by_criteria(sport, criteria)`: Get games filtered by multiple criteria such as team name, date range, bookmaker, and odds range.
3. A query engine for natural language processing of user queries.
