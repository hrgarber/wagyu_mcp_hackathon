# JavaScript Odds API Implementation: Complete Item List

## From oddsClient.js

### Classes:
* `OddsAPIClient` - Main client class for the Odds API

### Class Methods:
* `OddsAPIClient.constructor(apiKey)` - Initializes client with API key
* `OddsAPIClient.getSports()` - Gets all available sports
* `OddsAPIClient.getOdds(sport, options)` - Gets odds for specific sport
* `OddsAPIClient.makeRequest(endpoint, params)` - Core HTTP request method

### Standalone Functions:
* `getNextTestNumber()` - Gets next sequential test number for output directory
* `saveResponse(filename, data, testNumber)` - Saves API response to JSON file
* `testOddsAPI()` - Example function that demonstrates full API workflow
* `module.exports` - Exports the client class and test function

## From test.js

### Functions:
* `testOddsAPI()` - Simplified direct API test implementation 

### Variables:
* `API_KEY` - API key loaded from environment variables

## From load_json_data.py (Existing Python)

### Functions:
* `load_json_files()` - Loads saved JSON response files
* `print_summary(available_sports, nba_odds)` - Prints summary of loaded data
* `__main__` block - Script execution entry point

## Dependencies:
* `dotenv` - For loading environment variables
* `axios` - For making HTTP requests
* `fs` - Node.js filesystem module
* `path` - Node.js path module

## API Endpoints Used:
* `/sports` - For listing all sports
* `/sports/{sport}/odds` - For getting odds for a specific sport

## Request Parameters:
* `apiKey` - For authentication
* `regions` - Region for bookmakers data
* `markets` - Types of betting markets
* `oddsFormat` - Format for displaying odds

## Response Data Tracked:
* `x-requests-remaining` - Header for API quota management
* `x-requests-used` - Header for API quota usage
