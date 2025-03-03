# Granular API Methods

## Overview

The current `OddsClient` class provides broad methods that can consume multiple API credits in a single call. By adding more granular methods, we can give users precise control over API usage and credit consumption.

## Implementation

We'll create a new `endpoints/handlers.py` file with endpoint-specific handlers:

```python
"""
Endpoint-specific handlers for The Odds API.
"""
from typing import Dict, Any, Optional

class EndpointHandlers:
    """Handlers for specific API endpoints to optimize credit usage."""
    
    def __init__(self, client):
        """
        Initialize with a reference to the parent client.
        
        Args:
            client: OddsClient instance
        """
        self.client = client
    
    def get_sport_by_key(self, sport_key: str) -> Dict[str, Any]:
        """
        Get data for a single sport.
        
        Credit cost: 0
        
        Args:
            sport_key: Sport key to fetch
            
        Returns:
            API response data
        """
        return self.client.make_request("/sports")
    
    def get_specific_event_odds(self, sport_key: str, event_id: str, 
                               markets: str = "h2h", regions: str = "us") -> Dict[str, Any]:
        """
        Get odds for a specific event.
        
        Credit cost: [number of markets] × [number of regions]
        
        Args:
            sport_key: Sport key
            event_id: Specific event ID
            markets: Comma-separated list of markets
            regions: Comma-separated list of regions
            
        Returns:
            API response data
        """
        endpoint = f"/sports/{sport_key}/events/{event_id}/odds"
        params = {"markets": markets, "regions": regions}
        return self.client.make_request(endpoint, params)

    def get_minimal_odds(self, sport_key: str, regions: str = "us") -> Dict[str, Any]:
        """
        Get odds with minimal credit usage (1 credit).
        
        Credit cost: 1 (using single market and region)
        
        Args:
            sport_key: Sport key
            regions: Region code
            
        Returns:
            API response data
        """
        return self.client.make_request(f"/sports/{sport_key}/odds", 
                                       {"markets": "h2h", "regions": regions})
                                       
    def get_events_list(self, sport_key: str) -> Dict[str, Any]:
        """
        Get list of events for a sport.
        
        Credit cost: 0
        
        Args:
            sport_key: Sport key
            
        Returns:
            API response data
        """
        return self.client.make_request(f"/sports/{sport_key}/events")
```

## Integration with OddsClient

We'll integrate these handlers into the main `OddsClient` class:

```python
def __init__(self, api_key: str, **kwargs):
    # Existing initialization...
    
    # Set up endpoint handlers
    self.endpoints = EndpointHandlers(self)

# Example usage in client code
def get_sport_info(self, sport_key: str) -> Dict[str, Any]:
    """Get information about a specific sport (0 credit cost)."""
    return self.endpoints.get_sport_by_key(sport_key)
```

## Benefits

1. **Credit Efficiency**: Users can make precise API calls that use minimal credits
2. **Clear Documentation**: Each method clearly documents its credit cost
3. **Simplified Usage**: Methods are named according to their purpose
4. **Type Hints**: Proper type annotations for better IDE support
