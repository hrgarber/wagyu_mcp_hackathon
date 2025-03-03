# Response Archive System

## Overview

Instead of a traditional time-based cache, we'll implement a permanent archive of API responses. This will serve as a "golden dataset" for testing and mocking, allowing developers to work with consistent data without consuming API credits.

## Implementation

We'll create a dedicated `ResponseArchive` class:

```python
"""
Response archiving system for Wagyu Sports API.
"""
import json
import os
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional

class ResponseArchive:
    """Persistent archive of API responses for testing and reduced API usage."""
    
    def __init__(self, archive_dir: str = None):
        """
        Initialize the response archive.
        
        Args:
            archive_dir: Directory to store response files (defaults to 'responses' in package directory)
        """
        if archive_dir is None:
            # Default to 'responses' directory in the package
            package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.archive_dir = os.path.join(package_dir, "responses")
        else:
            self.archive_dir = archive_dir
            
        # Ensure directory exists
        os.makedirs(self.archive_dir, exist_ok=True)
        
        # Create subdirectories for different endpoints
        self.sports_dir = os.path.join(self.archive_dir, "sports")
        self.odds_dir = os.path.join(self.archive_dir, "odds")
        self.scores_dir = os.path.join(self.archive_dir, "scores")
        self.events_dir = os.path.join(self.archive_dir, "events")
        
        for directory in [self.sports_dir, self.odds_dir, self.scores_dir, self.events_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def get_filepath(self, endpoint: str, params: Dict[str, Any]) -> str:
        """
        Generate a filepath for a specific API request.
        
        Args:
            endpoint: API endpoint
            params: Request parameters
            
        Returns:
            Path to the response file
        """
        # Determine base directory based on endpoint
        if endpoint.startswith("/sports") and "/odds" not in endpoint and "/scores" not in endpoint:
            base_dir = self.sports_dir
        elif "/odds" in endpoint:
            base_dir = self.odds_dir
        elif "/scores" in endpoint:
            base_dir = self.scores_dir
        elif "/events" in endpoint:
            base_dir = self.events_dir
        else:
            # Use main directory for other endpoints
            base_dir = self.archive_dir
            
        # Create a stable representation of parameters
        param_str = json.dumps(params, sort_keys=True)
        
        # Create a hash of endpoint and parameters for filename
        hash_value = hashlib.md5(f"{endpoint}:{param_str}".encode()).hexdigest()
        
        # Create descriptive filename components
        components = []
        
        # Add sport key if present
        if "/sports/" in endpoint:
            sport_key = endpoint.split("/sports/")[1].split("/")[0]
            components.append(sport_key)
            
        # Add markets if present in params
        if "markets" in params:
            markets = params["markets"].replace(",", "_")
            components.append(f"markets-{markets}")
            
        # Add regions if present
        if "regions" in params:
            regions = params["regions"].replace(",", "_")
            components.append(f"regions-{regions}")
        
        # Construct filename with components and hash
        if components:
            filename = f"{'_'.join(components)}-{hash_value}.json"
        else:
            filename = f"{hash_value}.json"
            
        return os.path.join(base_dir, filename)
    
    def exists(self, endpoint: str, params: Dict[str, Any]) -> bool:
        """
        Check if a response exists in the archive.
        
        Args:
            endpoint: API endpoint
            params: Request parameters
            
        Returns:
            True if response exists
        """
        filepath = self.get_filepath(endpoint, params)
        return os.path.exists(filepath)
    
    def get(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Retrieve a response from the archive if it exists.
        
        Args:
            endpoint: API endpoint
            params: Request parameters
            
        Returns:
            Archived response or None if not found
        """
        filepath = self.get_filepath(endpoint, params)
        
        if not os.path.exists(filepath):
            return None
            
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # If file is corrupted or can't be read, return None
            return None
    
    def save(self, endpoint: str, params: Dict[str, Any], data: Dict[str, Any]) -> str:
        """
        Save a response to the archive.
        
        Args:
            endpoint: API endpoint
            params: Request parameters
            data: Response data
            
        Returns:
            Path to the saved file
        """
        filepath = self.get_filepath(endpoint, params)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return filepath
        except IOError as e:
            print(f"Error saving response to archive: {str(e)}")
            return ""
    
    def list_responses(self) -> Dict[str, int]:
        """
        Get statistics about archived responses.
        
        Returns:
            Dictionary with counts for each endpoint type
        """
        return {
            "sports": len(os.listdir(self.sports_dir)),
            "odds": len(os.listdir(self.odds_dir)),
            "scores": len(os.listdir(self.scores_dir)),
            "events": len(os.listdir(self.events_dir)),
            "other": len([f for f in os.listdir(self.archive_dir) 
                         if os.path.isfile(os.path.join(self.archive_dir, f))])
        }
```

## Integration with OddsClient

We'll integrate the archive system into the `OddsClient` class:

```python
def __init__(self, api_key: str, **kwargs):
    """
    Initialize the Wagyu Sports client.
    
    Args:
        api_key (str): API key for authentication with The Odds API
        **kwargs: Additional configuration options
    """
    self.api_key = api_key
    self.remaining_requests = None
    self.used_requests = None
    
    # Configure default settings
    self.default_region = kwargs.get('default_region', self.DEFAULT_REGION)
    self.default_markets = kwargs.get('default_markets', self.DEFAULT_MARKETS)
    self.default_date_format = kwargs.get('default_date_format', self.DEFAULT_DATE_FORMAT)
    self.default_odds_format = kwargs.get('default_odds_format', self.DEFAULT_ODDS_FORMAT)
    
    # Set up response archiving
    self.use_archive = kwargs.get('use_archive', True)
    archive_dir = kwargs.get('archive_dir')
    
    if self.use_archive:
        self.archive = ResponseArchive(archive_dir)
    else:
        self.archive = None

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
        
    # Validate parameters if appropriate
    if '/odds' in endpoint:
        valid, error_message = self.validator.validate_odds_params(params)
        if not valid:
            raise ValueError(f"Invalid parameters: {error_message}")
    
    # Estimate credit cost
    estimated_cost = utils.estimate_request_cost(endpoint, params)
        
    # Check archive if enabled - ALWAYS use archived response if it exists
    if self.use_archive:
        archived_response = self.archive.get(endpoint, params)
        if archived_response:
            return archived_response
            
    # Make actual request since we don't have an archived version
    # Add API key to params for the actual request
    request_params = params.copy()
    request_params["apiKey"] = self.api_key
            
    # Make actual request
    url = f"{self.BASE_URL}{endpoint}"
    response = requests.get(url, params=request_params)
    
    # Update header information
    if 'x-requests-remaining' in response.headers:
        self.remaining_requests = response.headers['x-requests-remaining']
    if 'x-requests-used' in response.headers:
        self.used_requests = response.headers['x-requests-used']
    
    # Raise exception for error status codes
    response.raise_for_status()
    
    # Process result
    result = {
        "data": response.json(),
        "headers": {
            "x-requests-remaining": self.remaining_requests,
            "x-requests-used": self.used_requests
        }
    }
    
    # Archive result if enabled
    if self.use_archive:
        self.archive.save(endpoint, params, result)
        
    return result
```

## Mock Testing Support

We'll add a special mode for testing that forces use of archived responses:

```python
def enable_mock_mode(self):
    """Enable mock mode - only use archived responses, never make actual API calls."""
    self.mock_mode = True
    
def disable_mock_mode(self):
    """Disable mock mode - allow actual API calls."""
    self.mock_mode = False
    
def make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    # Beginning of the method...
    
    # Check archive if enabled
    if self.use_archive:
        archived_response = self.archive.get(endpoint, params)
        if archived_response:
            return archived_response
            
    # If in mock mode and no archived response, raise an error
    if getattr(self, 'mock_mode', False):
        raise ValueError(f"No archived response for {endpoint} with params {params} (mock mode enabled)")
    
    # Continue with actual API request...
```

## Benefits

1. **Permanent Record**: Every unique request is saved permanently
2. **No Expirations**: Archived responses never expire
3. **Organized Structure**: Responses are organized by endpoint type
4. **Testing Support**: Perfect for creating mock tests
5. **Human-Readable**: File structure and names are designed to be human-readable
6. **Zero API Credits**: Once archived, responses can be reused without consuming API credits
