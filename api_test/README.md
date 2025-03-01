# The Odds API Testing Repository

This repository contains a testing environment for The Odds API, which will be used to develop the WagyuSports MCP (Model Context Protocol) server.

## Project Structure

```
.
├── oddsClient.js      # API client wrapper class
├── test.js           # Initial API test script
├── test_outputs/     # API response outputs
│   ├── test1/        # Basic API response tests
│   └── test2/        # Client wrapper tests
├── .env              # API key configuration
└── .gitignore        # Git ignore configuration
```

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file with your API key:
```
ODDS_API_KEY=your_api_key_here
```

## API Client Usage

The `oddsClient.js` provides a wrapper class for The Odds API with the following methods:

```javascript
const client = new OddsAPIClient(apiKey);

// Get list of available sports
const sports = await client.getSports();

// Get odds for a specific sport
const odds = await client.getOdds('basketball_nba', {
    regions: 'us',
    markets: 'h2h,spreads',
    oddsFormat: 'american'
});
```

## Test Results

- `test1/`: Contains raw API responses from initial testing
- `test2/`: Contains structured responses using the OddsAPIClient wrapper

## API Quota

The free tier of The Odds API includes:
- 500 requests per month
- Current usage is tracked in the client responses

## Notes

This repository is part of the WagyuSports MCP project, which aims to create a seamless bridge between sports bettors and real-time odds data through the Model Context Protocol.