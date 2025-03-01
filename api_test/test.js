require('dotenv').config();
const axios = require('axios');
const fs = require('fs');

// Get API key from .env file
const API_KEY = process.env.ODDS_API_KEY;

async function testOddsAPI() {
    if (!API_KEY) {
        console.error('Error: ODDS_API_KEY not found in .env file');
        return;
    }

    try {
        // Get NBA odds
        const response = await axios.get('https://api.the-odds-api.com/v4/sports/basketball_nba/odds', {
            params: {
                apiKey: API_KEY,
                regions: 'us',
                markets: 'h2h,spreads',
                oddsFormat: 'american'
            }
        });
        
        // Write response to file
        const output = {
            odds: response.data,
            remainingRequests: response.headers['x-requests-remaining']
        };
        
        fs.writeFileSync('nba_odds.json', JSON.stringify(output, null, 2));
        console.log('NBA odds written to nba_odds.json');
        
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
    }
}

// Run the test
testOddsAPI();