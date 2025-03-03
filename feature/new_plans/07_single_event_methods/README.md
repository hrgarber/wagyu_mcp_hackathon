# Single-Event Focus Methods

## Overview

To minimize API credit usage, we'll add methods that focus on single events rather than fetching data for multiple events at once.

## Implementation

We'll add these methods to the `endpoints/handlers.py` file:

```python
def follow_event(self, sport_key: str, event_id: str) -> Dict[str, Any]:
    """
    Get comprehensive data for a single event.
    
    Credit cost: 1-2 depending on configuration
    
    Args:
        sport_key: Sport key
        event_id: Event ID
        
    Returns:
        Combined event data
    """
    # Get scores first (if available)
    scores_response = self.client.make_request(f"/sports/{sport_key}/scores", 
                                              {"eventIds": event_id})
    
    # Then get odds for minimal markets to save credits
    odds_response = self.client.make_request(f"/sports/{sport_key}/events/{event_id}/odds", 
                                            {"markets": "h2h", "regions": self.client.default_region})
    
    # Combine the responses
    return {
        "event_details": scores_response.get("data", [{}])[0],
        "odds": odds_response.get("data", {})
    }

def get_event_details(self, sport_key: str, event_id: str) -> Dict[str, Any]:
    """
    Get basic details for a specific event without odds.
    
    Credit cost: 0
    
    Args:
        sport_key: Sport key
        event_id: Event ID
        
    Returns:
        Event details
    """
    response = self.client.make_request(f"/sports/{sport_key}/events", 
                                       {"eventIds": event_id})
    
    # Return the first (and should be only) event
    events = response.get("data", [])
    if not events:
        return {"error": "Event not found"}
        
    return events[0]

def get_event_odds_minimal(self, sport_key: str, event_id: str) -> Dict[str, Any]:
    """
    Get odds for a specific event with minimal credit usage.
    
    Credit cost: 1
    
    Args:
        sport_key: Sport key
        event_id: Event ID
        
    Returns:
        Event odds
    """
    return self.client.make_request(f"/sports/{sport_key}/events/{event_id}/odds", 
                                   {"markets": "h2h", "regions": self.client.default_region})
```

## Integration with OddsClient

We'll add convenience methods to the `OddsClient` class:

```python
def follow_event(self, sport_key: str, event_id: str) -> Dict[str, Any]:
    """
    Get comprehensive data for a single event.
    
    This method combines scores and odds data for a specific event,
    using minimal API credits.
    
    Credit cost: 1-2 depending on configuration
    
    Args:
        sport_key: Sport key
        event_id: Event ID
        
    Returns:
        Combined event data
    """
    return self.endpoints.follow_event(sport_key, event_id)
    
def get_event_details(self, sport_key: str, event_id: str) -> Dict[str, Any]:
    """
    Get basic details for a specific event without odds.
    
    Credit cost: 0
    
    Args:
        sport_key: Sport key
        event_id: Event ID
        
    Returns:
        Event details
    """
    return self.endpoints.get_event_details(sport_key, event_id)
    
def get_event_odds_minimal(self, sport_key: str, event_id: str) -> Dict[str, Any]:
    """
    Get odds for a specific event with minimal credit usage.
    
    Credit cost: 1
    
    Args:
        sport_key: Sport key
        event_id: Event ID
        
    Returns:
        Event odds
    """
    return self.endpoints.get_event_odds_minimal(sport_key, event_id)
```

## Example Usage

Here's how users can use these methods:

```python
from wagyu_sports import OddsClient
import os

# Initialize client
api_key = os.getenv("ODDS_API_KEY")
client = OddsClient(api_key)

# Get a list of events
events_response = client.endpoints.get_events_list("basketball_nba")
events = events_response["data"]

if events:
    # Get the first event ID
    event_id = events[0]["id"]
    
    # Get comprehensive data for this event (1-2 credits)
    event_data = client.follow_event("basketball_nba", event_id)
    
    # Print event details
    print(f"Event: {event_data['event_details']['home_team']} vs {event_data['event_details']['away_team']}")
    
    # Print odds
    if "bookmakers" in event_data["odds"]:
        bookmaker = event_data["odds"]["bookmakers"][0]
        print(f"Odds from {bookmaker['title']}:")
        for market in bookmaker["markets"]:
            print(f"  {market['key']}:")
            for outcome in market["outcomes"]:
                print(f"    {outcome['name']}: {outcome['price']}")
```

## Benefits

1. **Credit Efficiency**: Focus on specific events to minimize API credit usage
2. **Targeted Data**: Get only the data you need for a specific event
3. **Combined Data**: Get both scores and odds in a single method call
4. **Clear Documentation**: Each method clearly documents its credit cost
5. **Convenience**: Simplified API for common use cases
