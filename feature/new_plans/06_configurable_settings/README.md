# Configurable Default Settings

## Overview

To make the client more flexible and user-friendly, we'll add configurable default settings that can be customized during initialization.

## Implementation

We'll enhance the `OddsClient` class with configurable defaults:

```python
class OddsClient:
    """
    Client for sports betting data.
    
    This class provides methods for fetching sports betting data including
    available sports and odds for specific sports.
    """
    
    BASE_URL = "https://api.the-odds-api.com/v4"
    
    # Default settings
    DEFAULT_REGION = "us"
    DEFAULT_MARKETS = "h2h"
    DEFAULT_DATE_FORMAT = "iso"
    DEFAULT_ODDS_FORMAT = "decimal"
    
    def __init__(self, api_key: str, **kwargs):
        """
        Initialize the Wagyu Sports client.
        
        Args:
            api_key (str): API key for authentication with The Odds API
            **kwargs: Additional configuration options including:
                - default_region: Default region code (default: "us")
                - default_markets: Default markets (default: "h2h")
                - default_date_format: Default date format (default: "iso")
                - default_odds_format: Default odds format (default: "decimal")
                - use_archive: Whether to use response archiving (default: True)
                - archive_dir: Directory for archived responses (default: None)
                - mock_mode: Whether to use mock mode (default: False)
                - debug_mode: Whether to enable debug logging (default: False)
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
            
        # Set up mock mode
        self.mock_mode = kwargs.get('mock_mode', False)
        
        # Set up debug mode
        self.debug_mode = kwargs.get('debug_mode', False)
            
        # Set up validators
        self.validator = ParameterValidator()
        
        # Set up endpoint handlers
        self.endpoints = EndpointHandlers(self)
```

## Using Default Settings

We'll update the methods to use these default settings when specific parameters aren't provided:

```python
def get_odds(self, sport: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Get odds for a specific sport.
    
    Args:
        sport (str): Sport key (e.g., 'basketball_nba')
        options (Dict[str, Any], optional): Additional options for the request. Defaults to None.
            
    Returns:
        Dict[str, Any]: Response containing odds data
        
    Raises:
        ValueError: If parameters are invalid
        requests.exceptions.RequestException: If the request fails
    """
    # Validate sport key
    valid, error_message = self.validator.validate_sport_key(sport)
    if not valid:
        raise ValueError(f"Invalid sport key: {error_message}")
        
    # Apply default options if not provided
    if options is None:
        options = {}
        
    if 'regions' not in options:
        options['regions'] = self.default_region
        
    if 'markets' not in options:
        options['markets'] = self.default_markets
        
    if 'dateFormat' not in options:
        options['dateFormat'] = self.default_date_format
        
    if 'oddsFormat' not in options:
        options['oddsFormat'] = self.default_odds_format
        
    endpoint = f"/sports/{sport}/odds"
    return self.make_request(endpoint, options)
```

## Configuration Methods

We'll also add methods to update configuration at runtime:

```python
def set_default_region(self, region: str) -> None:
    """
    Set the default region.
    
    Args:
        region: Region code
        
    Raises:
        ValueError: If region is invalid
    """
    valid_regions = ['us', 'us2', 'uk', 'au', 'eu']
    if region not in valid_regions:
        raise ValueError(f"Invalid region: {region}. Valid regions are: {', '.join(valid_regions)}")
        
    self.default_region = region
    
def set_default_markets(self, markets: str) -> None:
    """
    Set the default markets.
    
    Args:
        markets: Comma-separated list of markets
        
    Raises:
        ValueError: If markets is empty
    """
    if not markets:
        raise ValueError("Markets cannot be empty")
        
    self.default_markets = markets
    
def set_default_date_format(self, date_format: str) -> None:
    """
    Set the default date format.
    
    Args:
        date_format: Date format
        
    Raises:
        ValueError: If date format is invalid
    """
    valid, error_message = self.validator.validate_date_format(date_format)
    if not valid:
        raise ValueError(error_message)
        
    self.default_date_format = date_format
    
def set_default_odds_format(self, odds_format: str) -> None:
    """
    Set the default odds format.
    
    Args:
        odds_format: Odds format
        
    Raises:
        ValueError: If odds format is invalid
    """
    valid, error_message = self.validator.validate_odds_format(odds_format)
    if not valid:
        raise ValueError(error_message)
        
    self.default_odds_format = odds_format
```

## Debug Mode

The debug mode setting enables additional logging:

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
        ValueError: If parameters are invalid
    """
    if params is None:
        params = {}
        
    # Validate parameters...
    
    # Estimate credit cost
    estimated_cost = utils.estimate_request_cost(endpoint, params)
    
    # Log request details if debug mode is enabled
    if self.debug_mode:
        print(f"Request: {endpoint}")
        print(f"Parameters: {params}")
        print(f"Estimated credit cost: {estimated_cost}")
    
    # Continue with the request...
```

## Benefits

1. **Flexibility**: Users can customize default behavior
2. **Convenience**: Reduces the need to specify the same parameters repeatedly
3. **Runtime Configuration**: Settings can be changed during runtime
4. **Debugging Support**: Debug mode for troubleshooting
5. **Consistent Defaults**: Ensures consistent behavior across the application
