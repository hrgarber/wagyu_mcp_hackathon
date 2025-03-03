#!/usr/bin/env python3
"""
Wagyu Sports Client Module

This module provides a client for interacting with sports betting data APIs.
"""
import requests
from typing import Dict, List, Optional, Any, Union


class OddsClient:
    """
    Client for sports betting data.
    
    This class provides methods for fetching sports betting data including
    available sports and odds for specific sports.
    """
    
    BASE_URL = "https://api.the-odds-api.com/v4"
    
    def __init__(self, api_key: str):
        """
        Initialize the Wagyu Sports client.
        
        Args:
            api_key (str): API key for authentication with The Odds API
        """
        self.api_key = api_key
        self.remaining_requests = None
        self.used_requests = None
    
    def get_sports(self, all_sports: bool = False) -> Dict[str, Any]:
        """
        Get a list of available sports.
        
        Args:
            all_sports (bool, optional): Include out-of-season sports. Defaults to False.
            
        Returns:
            Dict[str, Any]: Response containing available sports data
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        params = {"apiKey": self.api_key}
        if all_sports:
            params["all"] = "true"
            
        return self.make_request("/sports", params)
    
    def get_odds(self, sport: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get odds for a specific sport.
        
        Args:
            sport (str): Sport key (e.g., 'basketball_nba')
            options (Dict[str, Any], optional): Additional options for the request. Defaults to None.
                Possible options include:
                - regions: Comma-separated list of regions (e.g., 'us,uk')
                - markets: Comma-separated list of markets (e.g., 'h2h,spreads')
                - oddsFormat: Format for odds ('decimal' or 'american')
                - dateFormat: Format for dates ('unix' or 'iso')
                
        Returns:
            Dict[str, Any]: Response containing odds data
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        endpoint = f"/sports/{sport}/odds"
        params = {"apiKey": self.api_key}
        
        if options:
            params.update(options)
            
        return self.make_request(endpoint, params)
    
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
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, params=params)
        
        # Store quota information from headers
        if 'x-requests-remaining' in response.headers:
            self.remaining_requests = response.headers['x-requests-remaining']
        if 'x-requests-used' in response.headers:
            self.used_requests = response.headers['x-requests-used']
        
        # Raise exception for error status codes
        response.raise_for_status()
        
        # Return JSON response
        return {
            "data": response.json(),
            "headers": {
                "x-requests-remaining": self.remaining_requests,
                "x-requests-used": self.used_requests
            }
        }
