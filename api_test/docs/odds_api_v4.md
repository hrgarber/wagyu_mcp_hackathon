# The Odds API v4 Documentation

## Overview
The Odds API provides comprehensive access to sports betting data, including live odds, scores, and event information from multiple bookmakers worldwide. This document serves as a detailed reference for the API's capabilities and integration points.

## Base URL
- Primary: `https://api.the-odds-api.com`
- IPv6: `https://ipv6-api.the-odds-api.com`

## Authentication
- Requires an API key passed as query parameter `apiKey`
- Usage tracked through response headers:
  - `x-requests-remaining`: Credits remaining until quota reset
  - `x-requests-used`: Credits used since last quota reset
  - `x-requests-last`: Usage cost of last API call

## Available Endpoints

### 1. Sports List
**Endpoint:** `GET /v4/sports`
**Cost:** Free (doesn't count against quota)

**Capabilities:**
- List all in-season sports
- Option to include out-of-season sports
- Provides sport keys used in other endpoints

**Parameters:**
- `apiKey`: Required - API authentication key
- `all`: Optional - Include out-of-season sports if true

### 2. Odds Data
**Endpoint:** `GET /v4/sports/{sport}/odds`
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
- `commenceTimeFrom`: Optional - Filter by start time
- `commenceTimeTo`: Optional - Filter by end time
- `includeLinks`: Optional - Include bookmaker links
- `includeSids`: Optional - Include source IDs
- `includeBetLimits`: Optional - Include betting limits

### 3. Scores
**Endpoint:** `GET /v4/sports/{sport}/scores`
**Cost:** 1-2 credits depending on parameters

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

### 4. Events
**Endpoint:** `GET /v4/sports/{sport}/events`
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
- `commenceTimeFrom`: Optional - Start time filter
- `commenceTimeTo`: Optional - End time filter

### 5. Event-Specific Odds
**Endpoint:** `GET /v4/sports/{sport}/events/{eventId}/odds`
**Cost:** Varies based on markets and regions

**Capabilities:**
- Detailed odds for single events
- All available betting markets
- Market-specific descriptions
- Granular market updates
- Same parameter options as main odds endpoint

## Integration Notes

### Quota Management
- Track usage through response headers
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

## Example Use Cases

1. **Live Odds Tracking**
   - Monitor odds movements
   - Compare bookmaker prices
   - Track market changes

2. **Score Updates**
   - Live game tracking
   - Historical results analysis
   - Match status monitoring

3. **Event Discovery**
   - Upcoming game schedules
   - Sport-specific calendars
   - Regional event filtering

4. **Market Analysis**
   - Cross-bookmaker comparison
   - Arbitrage opportunity detection
   - Historical odds analysis

5. **Betting Exchange Integration**
   - Back/Lay odds monitoring
   - Bet limits tracking
   - Exchange-specific features

## Error Handling
- API returns standard HTTP status codes
- Error messages include descriptive text
- Quota exceeded returns specific error
- Invalid parameters clearly identified
- Rate limiting information included

## Rate Limiting
- Quota reset period defined by subscription
- Usage tracked per endpoint
- Some endpoints exempt from quota
- Multiple markets/regions affect usage
- Remaining quota in response headers