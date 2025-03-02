#!/usr/bin/env python3
"""
Enhanced Odds API Client Module

This module extends the base OddsClient with a method to get sports
available for betting tonight in a specific region.
"""
import sys
import os
from datetime import datetime, timezone, time, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
import pytz

# Add the parent directory to the path so we can import the python_odds_api package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from api_test.python_odds_api import OddsClient


class EnhancedOddsClient(OddsClient):
    """
    Enhanced client for The Odds API v4.
    
    This class extends the base OddsClient with additional methods for more
    specific and dynamic queries.
    """
    
    def get_available_sports_tonight(
        self, 
        region: str = "us", 
        start_time: Optional[datetime] = None, 
        end_time: Optional[datetime] = None,
        timezone_str: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get sports that have games available for betting between the specified times in the specified region.
        
        Args:
            region (str, optional): Region to check for betting availability. Defaults to "us".
            start_time (datetime, optional): Start time for filtering games. Defaults to current time.
            end_time (datetime, optional): End time for filtering games. Defaults to 11:59 PM local time.
            timezone_str (str, optional): Timezone to use for time calculations. Defaults to local timezone.
                
        Returns:
            Dict[str, Any]: Response containing sports with games available in the specified time range
        """
        # Get all available sports
        sports_response = self.get_sports(all_sports=False)  # Only active sports
        
        # Determine the timezone to use
        if timezone_str:
            try:
                local_tz = pytz.timezone(timezone_str)
            except pytz.exceptions.UnknownTimeZoneError:
                # Fall back to UTC if timezone is unknown
                local_tz = pytz.UTC
        else:
            # Default to America/Los_Angeles (PST/PDT) if no timezone specified
            local_tz = pytz.timezone('America/Los_Angeles')
        
        # Get current date and time in the local timezone
        now_utc = datetime.now(timezone.utc)
        now_local = now_utc.astimezone(local_tz)
        today_local = now_local.date()
        
        # Use provided start_time or default to current time in the local timezone
        if start_time is None:
            start_time_local = now_local
        else:
            # Convert to the local timezone if it has a timezone, otherwise assume it's in the local timezone
            if start_time.tzinfo:
                start_time_local = start_time.astimezone(local_tz)
            else:
                start_time_local = local_tz.localize(start_time)
        
        # Use provided end_time or default to 11:59 PM today in the local timezone
        if end_time is None:
            end_time_local = datetime.combine(
                today_local, 
                time(23, 59, 59), 
                tzinfo=local_tz
            )
        else:
            # Convert to the local timezone if it has a timezone, otherwise assume it's in the local timezone
            if end_time.tzinfo:
                end_time_local = end_time.astimezone(local_tz)
            else:
                end_time_local = local_tz.localize(end_time)
        
        # Convert local times back to UTC for API comparison
        start_time_utc = start_time_local.astimezone(timezone.utc)
        end_time_utc = end_time_local.astimezone(timezone.utc)
        
        available_sports = []
        
        # Check each sport for games tonight
        for sport in sports_response['data']:
            sport_key = sport.get('key')
            
            try:
                # Try to get odds for this sport in the specified region
                options = {
                    "regions": region,
                    "dateFormat": "iso"
                }
                
                odds_response = self.get_odds(sport_key, options)
                
                # Check if there are any games starting between start_time and end_time
                has_games_tonight = False
                games_tonight = []
                
                for game in odds_response['data']:
                    if 'commence_time' in game:
                        try:
                            # Parse the UTC time from the API
                            game_time_utc = datetime.fromisoformat(
                                game['commence_time'].replace('Z', '+00:00')
                            )
                            
                            # Check if the game is within our UTC time window
                            if start_time_utc <= game_time_utc <= end_time_utc:
                                has_games_tonight = True
                                
                                # Add local time to the game for display purposes
                                game_time_local = game_time_utc.astimezone(local_tz)
                                game_copy = game.copy()
                                game_copy['commence_time_local'] = game_time_local.isoformat()
                                games_tonight.append(game_copy)
                        except (ValueError, TypeError):
                            # Skip games with invalid datetime
                            continue
                
                if has_games_tonight:
                    # Sort games by commence time
                    games_tonight.sort(key=lambda g: datetime.fromisoformat(
                        g['commence_time'].replace('Z', '+00:00')
                    ))
                    
                    sport_info = sport.copy()
                    sport_info['games_count'] = len(games_tonight)
                    sport_info['sample_game'] = games_tonight[0] if games_tonight else None
                    sport_info['timezone'] = str(local_tz)
                    
                    available_sports.append(sport_info)
            
            except Exception as e:
                # If we can't get odds for this sport, skip it
                continue
        
        # Return the filtered results with the same header information
        return {
            "data": available_sports,
            "headers": sports_response['headers'],
            "time_window": {
                "start_time_local": start_time_local.isoformat(),
                "end_time_local": end_time_local.isoformat(),
                "timezone": str(local_tz)
            }
        }
