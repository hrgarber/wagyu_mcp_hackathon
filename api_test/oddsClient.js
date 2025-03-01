require('dotenv').config();
const axios = require('axios');
const fs = require('fs');
const path = require('path');

class OddsAPIClient {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseURL = 'https://api.the-odds-api.com/v4';
        this.requestCount = 0;
    }

    // Get all available sports
    async getSports() {
        return this.makeRequest('/sports');
    }

    // Get odds for a specific sport
    async getOdds(sport, { regions = 'us', markets = 'h2h,spreads', oddsFormat = 'american' } = {}) {
        return this.makeRequest(`/sports/${sport}/odds`, {
            regions,
            markets,
            oddsFormat
        });
    }

    // Make API request
    async makeRequest(endpoint, params = {}) {
        try {
            const response = await axios.get(`${this.baseURL}${endpoint}`, {
                params: {
                    apiKey: this.apiKey,
                    ...params
                }
            });

            this.requestCount++;
            return {
                data: response.data,
                remaining: response.headers['x-requests-remaining'],
                used: response.headers['x-requests-used']
            };
        } catch (error) {
            if (error.response) {
                throw new Error(`API Error: ${error.response.status} - ${JSON.stringify(error.response.data)}`);
            }
            throw error;
        }
    }
}

// Get the next test number
function getNextTestNumber() {
    const baseDir = path.join(process.cwd(), 'test_outputs');
    if (!fs.existsSync(baseDir)) {
        return 1;
    }

    const testDirs = fs.readdirSync(baseDir)
        .filter(name => name.startsWith('test'))
        .map(name => parseInt(name.replace('test', '')))
        .filter(num => !isNaN(num));

    return testDirs.length > 0 ? Math.max(...testDirs) + 1 : 1;
}

// Save response to file
function saveResponse(filename, data, testNumber) {
    const outputDir = path.join(process.cwd(), 'test_outputs', `test${testNumber}`);
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }
    const filePath = path.join(outputDir, filename);
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
    console.log(`Results saved to: ${filePath}`);
}

// Example usage
async function testOddsAPI() {
    const client = new OddsAPIClient(process.env.ODDS_API_KEY);
    const testNumber = getNextTestNumber();

    try {
        // Get all sports (1 request)
        console.log('\nFetching available sports...');
        const sports = await client.getSports();
        console.log(`Found ${sports.data.length} sports`);
        console.log(`API Requests used: ${client.requestCount}`);
        console.log(`Requests remaining: ${sports.remaining}`);
        saveResponse('1_available_sports.json', sports, testNumber);

        // Get NBA odds (1 request)
        console.log('\nFetching NBA odds...');
        const nbaOdds = await client.getOdds('basketball_nba');
        console.log(`Found ${nbaOdds.data.length} games`);
        console.log(`API Requests used: ${client.requestCount}`);
        console.log(`Requests remaining: ${nbaOdds.remaining}`);
        saveResponse('2_nba_odds.json', nbaOdds, testNumber);

    } catch (error) {
        console.error('Error:', error.message);
        saveResponse('error_log.json', {
            timestamp: new Date().toISOString(),
            error: error.message,
            requestsUsed: client.requestCount
        }, testNumber);
    }
}

// Export the client class and test function
module.exports = {
    OddsAPIClient,
    testOddsAPI
};

// Run test if this file is run directly
if (require.main === module) {
    testOddsAPI();
}