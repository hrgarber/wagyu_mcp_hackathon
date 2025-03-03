# Request Parameter Validation

## Overview

To prevent errors and wasted API credits, we'll add parameter validation to ensure that all requests are properly formed before they're sent to the API.

## Implementation

We'll create a dedicated `validators/params.py` file:

```python
"""
Parameter validation for API requests.
"""
from typing import Dict, Any, Tuple, List, Optional

class ParameterValidator:
    """Validates API request parameters to prevent errors and wasted credits."""
    
    @staticmethod
    def validate_odds_params(params: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate parameters for odds endpoints.
        
        Args:
            params: Request parameters
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for empty markets
        if 'markets' in params and not params['markets']:
            return False, "Markets parameter cannot be empty"
            
        # Check for empty regions
        if 'regions' in params and not params['regions']:
            return False, "Regions parameter cannot be empty"
            
        # Check for valid region codes
        if 'regions' in params:
            valid_regions = ['us', 'us2', 'uk', 'au', 'eu']
            regions = params['regions'].split(',')
            invalid_regions = [r for r in regions if r not in valid_regions]
            
            if invalid_regions:
                return False, f"Invalid region codes: {', '.join(invalid_regions)}"
                
        return True, ""
    
    @staticmethod
    def validate_sport_key(sport_key: str) -> Tuple[bool, str]:
        """
        Validate sport key format.
        
        Args:
            sport_key: Sport key to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not sport_key:
            return False, "Sport key cannot be empty"
            
        # 'upcoming' is always valid
        if sport_key == 'upcoming':
            return True, ""
            
        # Basic format check
        if not all(c.isalnum() or c in ['_', '-'] for c in sport_key):
            return False, "Sport key contains invalid characters"
            
        return True, ""
        
    @staticmethod
    def validate_date_format(date_format: str) -> Tuple[bool, str]:
        """
        Validate date format parameter.
        
        Args:
            date_format: Date format to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        valid_formats = ['iso', 'unix']
        if date_format not in valid_formats:
            return False, f"Invalid date format: {date_format}. Valid formats are: {', '.join(valid_formats)}"
            
        return True, ""
        
    @staticmethod
    def validate_odds_format(odds_format: str) -> Tuple[bool, str]:
        """
        Validate odds format parameter.
        
        Args:
            odds_format: Odds format to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        valid_formats = ['decimal', 'american']
        if odds_format not in valid_formats:
            return False, f"Invalid odds format: {odds_format}. Valid formats are: {', '.join(valid_formats)}"
            
        return True, ""
```

## Integration with OddsClient

We'll integrate the validator into the `OddsClient` class:

```python
def __init__(self, api_key: str, **kwargs):
    # Existing initialization...
    
    # Set up validators
    self.validator = ParameterValidator()

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
        
    # Validate parameters based on endpoint
    if '/odds' in endpoint:
        valid, error_message = self.validator.validate_odds_params(params)
        if not valid:
            raise ValueError(f"Invalid parameters: {error_message}")
            
    # Validate date_format if present
    if 'dateFormat' in params:
        valid, error_message = self.validator.validate_date_format(params['dateFormat'])
        if not valid:
            raise ValueError(f"Invalid parameters: {error_message}")
            
    # Validate odds_format if present
    if 'oddsFormat' in params:
        valid, error_message = self.validator.validate_odds_format(params['oddsFormat'])
        if not valid:
            raise ValueError(f"Invalid parameters: {error_message}")
    
    # Continue with the request...
```

## Enhanced Endpoint Methods

We'll also add validation to the endpoint-specific methods:

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
        
    endpoint = f"/sports/{sport}/odds"
    return self.make_request(endpoint, options)
```

## Benefits

1. **Prevent Errors**: Catch invalid parameters before making API calls
2. **Save Credits**: Avoid wasted API credits on requests that would fail
3. **Better Error Messages**: Provide clear, specific error messages
4. **Consistent Validation**: Apply the same validation rules throughout the codebase
5. **Type Safety**: Proper type annotations for better IDE support
