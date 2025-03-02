# The Odds API v4 Documentation

## Overview
The Odds API provides comprehensive access to sports betting data, including live odds, scores, and event information from multiple bookmakers worldwide. This document serves as a detailed reference for the API's capabilities and integration points.

## Host
- Primary: `https://api.the-odds-api.com`
- IPv6: `https://ipv6-api.the-odds-api.com`

## Authentication
The Odds API uses API keys for authentication. All requests require an API key passed as a query parameter `apiKey`.

## Available Endpoints

### 1. Sports List (`GET /v4/sports`)
**Cost:** Free (doesn't count against quota)

**Capabilities:**
- List all in-season sports
- Option to include out-of-season sports
- Provides sport keys used in other endpoints

**Parameters:**
- `apiKey`: Required - API authentication key
- `all`: Optional - Include out-of-season sports if true

### 2. Odds Data (`GET /v4/sports/{sport}/odds`)
**Cost:** 1 credit per region per market

**Capabilities:**
- Fetch odds for upcoming and live games
- Multiple betting markets support
- Regional bookmaker coverage
- Customizable odds format
- Optional bet limits information
- Bookmaker deep linking

**Markets Available:**
- `h2h`: Head to head/moneyline
- `spreads`: Points handicaps
- `totals`: Over/under
- `outrights`: Futures
- `h2h_lay`: Lay odds (betting exchanges)
- `outrights_lay`: Outright lay odds

**Regions Available:**
- `us`: United States
- `us2`: United States (additional bookmakers)
- `uk`: United Kingdom
- `au`: Australia
- `eu`: Europe

**Parameters:**
- `sport`: Required - Sport key from sports list
- `regions`: Required - Comma-separated list of regions
- `markets`: Optional - Comma-separated list of markets (default: h2h)
- `dateFormat`: Optional - 'unix' or 'iso' (default: iso)
- `oddsFormat`: Optional - 'decimal' or 'american' (default: decimal)
- `eventIds`: Optional - Filter specific events
- `bookmakers`: Optional - Filter specific bookmakers
- `commenceTimeFrom`: Optional - Filter by start time (ISO 8601)
- `commenceTimeTo`: Optional - Filter by end time (ISO 8601)
- `includeLinks`: Optional - Include bookmaker links
- `includeSids`: Optional - Include source IDs
- `includeBetLimits`: Optional - Include betting limits

### 3. Scores (`GET /v4/sports/{sport}/scores`)
**Cost:** 
- 1 credit for live and upcoming games
- 2 credits when including historical data

**Capabilities:**
- Live scores (30-second updates)
- Historical scores (up to 3 days)
- Upcoming game schedules
- Detailed scoring information
- Match status tracking

**Parameters:**
- `sport`: Required - Sport key
- `daysFrom`: Optional - Historical data (1-3 days)
- `dateFormat`: Optional - 'unix' or 'iso'
- `eventIds`: Optional - Filter specific events

### 4. Events (`GET /v4/sports/{sport}/events`)
**Cost:** Free (doesn't count against quota)

**Capabilities:**
- List in-play and pre-match events
- Basic game information
- Team details
- Event scheduling
- Date range filtering

**Parameters:**
- `sport`: Required - Sport key
- `dateFormat`: Optional - 'unix' or 'iso'
- `eventIds`: Optional - Filter specific events
- `commenceTimeFrom`: Optional - Start time filter (ISO 8601)
- `commenceTimeTo`: Optional - End time filter (ISO 8601)

### 5. Event-Specific Odds (`GET /v4/sports/{sport}/events/{eventId}/odds`)
**Cost:** Varies based on markets and regions

**Capabilities:**
- Detailed odds for single events
- All available betting markets
- Market-specific descriptions
- Granular market updates
- Same parameter options as main odds endpoint

### 6. Participants (`GET /v4/sports/{sport}/participants`)
**Cost:** 1 credit

**Capabilities:**
- List all participants (teams or individuals) for a sport
- Does not include players on teams
- Includes both active and inactive participants

**Parameters:**
- `sport`: Required - Sport key
- `apiKey`: Required - API authentication key

### 7. Historical Odds (`GET /v4/historical/sports/{sport}/odds`)
**Cost:** 10 credits per region per market

**Capabilities:**
- Historical odds data from June 6th, 2020
- 10-minute intervals until September 2022
- 5-minute intervals after September 2022
- Available only on paid plans

**Parameters:**
- All parameters from the odds endpoint, plus:
- `date`: Required - Timestamp for historical data (ISO 8601)

### 8. Historical Events (`GET /v4/historical/sports/{sport}/events`)
**Cost:** 1 credit (free if no events found)

**Capabilities:**
- List historical events at a specified timestamp
- Includes event details without odds
- Useful for finding historical event IDs

**Parameters:**
- Same as events endpoint, plus:
- `date`: Required - Timestamp for historical data (ISO 8601)

### 9. Historical Event Odds (`GET /v4/historical/sports/{sport}/events/{eventId}/odds`)
**Cost:** 10 credits per region per market

**Capabilities:**
- Historical odds for a single event
- Support for all betting markets
- Additional markets available after May 3rd, 2023
- Available only on paid plans

**Parameters:**
- Same as event-specific odds endpoint, plus:
- `date`: Required - Timestamp for historical data (ISO 8601)

## Integration Notes

### Quota Management
- Track usage through response headers:
  - `x-requests-remaining`: Credits remaining until quota reset
  - `x-requests-used`: Credits used since last quota reset
  - `x-requests-last`: Usage cost of last API call
- Costs vary by endpoint and parameters
- Some endpoints are free
- Multiple markets/regions multiply quota cost

### Best Practices
1. Use free endpoints for basic data
2. Batch requests when possible
3. Cache responses when appropriate
4. Monitor quota usage headers
5. Use event-specific endpoint for detailed market data
6. Filter by eventIds to reduce data volume

### Data Updates
- Live scores update ~every 30 seconds
- Odds updates vary by market and bookmaker
- Events may become temporarily unavailable between rounds
- Completed events are removed from odds endpoints
- Historical scores available up to 3 days

### Special Features
1. **Betting Exchange Support**
   - Automatic lay odds inclusion
   - Bet limits information
   - Exchange-specific markets

2. **Deep Linking**
   - Bookmaker event links
   - Market-specific links
   - Betslip integration
   - Source IDs for custom linking

3. **Market Coverage**
   - Full coverage for major markets
   - Expanding coverage for additional markets
   - Sport-specific market availability
   - Regional variations in coverage

## Rate Limiting
- Requests are rate limited to protect systems
- Status code 429 indicates rate limit reached
- Space out requests over several seconds when rate limited
- Quota reset period defined by subscription
- Usage tracked per endpoint
- Some endpoints exempt from quota
- Multiple markets/regions affect usage
- Remaining quota in response headers

## Error Handling
- API returns standard HTTP status codes
- Error messages include descriptive text
- Quota exceeded returns specific error
- Invalid parameters clearly identified
- Rate limiting information included