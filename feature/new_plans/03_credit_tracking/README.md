# Credit Cost Tracking & Estimation

## Overview

The Odds API has a credit-based usage system, where different endpoints and parameters consume different amounts of credits. To help users manage their API usage efficiently, we'll add utilities for tracking and estimating credit costs.

## Implementation

We'll enhance `utils.py` with credit management utilities:

```python
"""
Utility functions for the Wagyu Sports client.
"""
import os
import json
import time
from typing import Dict, Any, Optional, Tuple

def estimate_request_cost(endpoint: str, params: Dict[str, Any] = None) -> int:
    """
    Estimate the API credit cost before making a request.
    
    Args:
        endpoint: API endpoint
        params: Request parameters
        
    Returns:
        Estimated credit cost
    """
    if params is None:
        params = {}
        
    # Sports endpoint is free
    if endpoint.startswith("/sports") and '/odds' not in endpoint:
        return 0
        
    # Odds endpoints cost scales with markets and regions
    if '/odds' in endpoint:
        markets = len(params.get('markets', 'h2h').split(','))
        regions = len(params.get('regions', 'us').split(','))
        
        # Historical odds cost more (10x)
        if '/historical/' in endpoint:
            return 10 * markets * regions
            
        return markets * regions
        
    # Scores endpoint
    if '/scores' in endpoint:
        return 2 if params.get('daysFrom') else 1
        
    # Default for other endpoints
    return 1

def format_credit_info(headers: Dict[str, str]) -> Dict[str, int]:
    """
    Format credit information from API response headers.
    
    Args:
        headers: API response headers
        
    Returns:
        Formatted credit information
    """
    return {
        "remaining": int(headers.get('x-requests-remaining', 0)),
        "used": int(headers.get('x-requests-used', 0)),
        "last_request": int(headers.get('x-requests-last', 0))
    }
```

## Integration with OddsClient

We'll add methods to the `OddsClient` class to expose these utilities:

```python
def estimate_request_cost(self, endpoint: str, params: Dict[str, Any] = None) -> int:
    """
    Estimate the credit cost of a request before making it.
    
    Args:
        endpoint: API endpoint
        params: Request parameters
        
    Returns:
        Estimated credit cost
    """
    return utils.estimate_request_cost(endpoint, params)

def get_remaining_credits(self) -> int:
    """
    Get remaining API credits (costs 0 credits).
    
    Returns:
        Number of remaining credits
    """
    response = self.endpoints.get_sport_by_key("upcoming")
    return int(response['headers'].get('x-requests-remaining', 0))
    
def get_credit_usage(self) -> Dict[str, int]:
    """
    Get detailed credit usage information.
    
    Returns:
        Dictionary with credit usage information
    """
    response = self.endpoints.get_sport_by_key("upcoming")
    return utils.format_credit_info(response['headers'])
```

## Enhanced make_request Method

We'll also enhance the `make_request` method to include credit cost estimation:

```python
def make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Make a request to the sports data API.
    
    Args:
        endpoint (str): API endpoint (e.g., '/sports')
        params (Dict[str, Any], optional): Query parameters. Defaults to None.
        
    Returns:
        Dict[str, Any]: Response data
        
    Raises:
        requests.exceptions.RequestException: If the request fails
    """
    if params is None:
        params = {}
        
    # Estimate credit cost
    estimated_cost = self.estimate_request_cost(endpoint, params)
    
    # Log the estimated cost if debug mode is enabled
    if getattr(self, 'debug_mode', False):
        print(f"Estimated credit cost for {endpoint}: {estimated_cost}")
    
    # Continue with the request...
```

## Benefits

1. **Cost Awareness**: Users can estimate costs before making requests
2. **Usage Monitoring**: Easy access to credit usage information
3. **Debugging Support**: Helps identify which calls are consuming credits
4. **Optimization Guidance**: Helps users optimize their API usage
