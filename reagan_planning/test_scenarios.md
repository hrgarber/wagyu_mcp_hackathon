# Sports Betting API Test Scenarios

## Introduction

This document outlines test scenarios for the sports betting API integration based on user research conducted with Reagan, an experienced sports bettor. The scenarios are designed to validate that our implementation meets the needs of different types of sports bettors, from casual fans to value shoppers.

These test scenarios will serve as a guide for implementing and testing our sports betting functionality, ensuring we deliver a product that addresses real user needs identified during our research.

## User Personas

Based on our interview with Reagan, we've identified several key user personas:

### 1. The Casual Game Night Bettor
- **Motivation**: Enhance enjoyment of a game they're already watching
- **Behavior**: Makes quick decisions based on basic odds
- **Needs**: Simple, clear presentation of standard odds (spread, moneyline, over/under)
- **Quote**: "I'm watching the Lakers game with friends and want to place a quick bet"

### 2. The Value Shopper
- **Motivation**: Find the best possible odds for a bet they want to make
- **Behavior**: Compares the same bet across multiple sportsbooks
- **Needs**: Cross-book comparison, especially for futures bets
- **Quote**: "I want to place a bet on Loyola Marymount at the highest possible odds"

### 3. The Browser/Shopper
- **Motivation**: Discover betting opportunities without a specific game in mind
- **Behavior**: Browses available games before deciding where to focus
- **Needs**: Comprehensive list of betting options, easy navigation
- **Quote**: "If I'm just hanging around on Saturday night like casually, I just wanna see what's option. I want to scroll almost like I want to shop."

### 4. The Trend Spotter
- **Motivation**: Identify value based on line movements and betting patterns
- **Behavior**: Looks for unusual activity or significant changes in odds
- **Needs**: Line movement data, bet distribution information
- **Quote**: "I want to see if there's unusual line movement on any games tonight"

## Test Scenarios

### Test Scenario 1: Sport Browsing Experience

**User Persona:** Browser/Shopper  
**Description:** User wants to see what betting options are available without a specific game in mind

**Test Inputs:**
1. "What sports are available to bet on right now?"
2. "Show me all available [SPORT] games for today" (where SPORT is one returned from first query)

**Expected Output for Input 1:**
```
Available Sports for Betting:
• NBA Basketball
• NHL Hockey
• MLB Baseball (if in season)
• Soccer (various leagues)
• [Other available sports]
```

**Expected Output for Input 2:**
```
Available [SPORT] Games Today:
• [Team A] vs [Team B] - [Time]
• [Team C] vs [Team D] - [Time]
• [Additional games with teams and times]
```

**Evaluation Criteria:**
- System correctly identifies available sports
- System lists current/upcoming games for selected sport
- Output includes essential information (teams, times)
- Response is well-formatted and easy to scan

### Test Scenario 2: Basic Game Odds Lookup

**User Persona:** Casual Game Night Bettor  
**Description:** User wants basic odds for a specific game they're watching or interested in

**Test Inputs:**
1. "What are the odds for the [specific game]?" (use first game from previous scenario)

**Expected Output:**
```
[Team A] vs [Team B] - [Time]
Caesars Sportsbook:

• Spread: [Team A] -4.5 (-110)
• Moneyline: [Team A] -190, [Team B] +160
• Over/Under: 224.5 (-110)
```

**Evaluation Criteria:**
- System displays all three standard bet types (spread, moneyline, over/under)
- Odds are shown in American format
- Default sportsbook is clearly identified
- Information is presented clearly and concisely

### Test Scenario 3: Cross-Book Value Shopping

**User Persona:** Value Shopper  
**Description:** User wants to compare odds across sportsbooks to find the best value

**Test Inputs:**
1. "What are the odds for [specific game]?" (same as Scenario 2)
2. "Compare those odds across all sportsbooks"
3. "Where can I get the best odds for [Team A]?"

**Expected Output for Input 2:**
```
[Team A] vs [Team B] - Odds Comparison:

Spread:
• Caesars: [Team A] -4.5 (-110)
• FanDuel: [Team A] -4 (-112)
• DraftKings: [Team A] -4.5 (-108)
• BetMGM: [Team A] -5 (-105)

Moneyline:
• Caesars: [Team A] -190, [Team B] +160
• FanDuel: [Team A] -185, [Team B] +155
• DraftKings: [Team A] -195, [Team B] +165
• BetMGM: [Team A] -200, [Team B] +170
```

**Expected Output for Input 3:**
```
Best odds for [Team A]:

• Spread: FanDuel ([Team A] -4)
• Moneyline: FanDuel ([Team A] -185)
```

**Evaluation Criteria:**
- System successfully retrieves odds from multiple sources
- Comparison is formatted in an easy-to-read manner
- System correctly identifies best value opportunities
- Response handles different bet types appropriately

### Test Scenario 4: Futures Bet Shopping

**User Persona:** Value Shopper (long-term)  
**Description:** User wants to compare futures odds across sportsbooks

**Test Inputs:**
1. "Show me futures odds for [league] championship"
2. "Which book has the best odds for [Team X]?" (where Team X is one from the response)

**Expected Output for Input 1:**
```
[League] Championship Winner Odds:

[Team X]:
• DraftKings: +450
• FanDuel: +425
• Caesars: +475
• BetMGM: +460

[Team Y]:
• DraftKings: +600
• FanDuel: +550
• Caesars: +575
• BetMGM: +590

[Additional teams with odds across books]
```

**Expected Output for Input 2:**
```
Best odds for [Team X] to win [League] Championship:
Caesars: +475 (Best value)
```

**Evaluation Criteria:**
- System retrieves futures/outrights market data
- Comparison includes multiple sportsbooks
- System identifies best value for specific selections
- Format highlights the variance between books

### Test Scenario 5: Advanced Filtering (Stretch Goal)

**User Persona:** Trend Spotter  
**Description:** User wants to find specific betting opportunities based on criteria

**Test Inputs:**
1. "Show me all [SPORT] underdogs with a spread of +5 or more"
2. "Which of these has the biggest difference in odds between sportsbooks?"

**Expected Output for Input 1:**
```
[SPORT] Underdogs (+5 or more):

• [Team B] +6 vs [Team A]
• [Team D] +7.5 vs [Team C]
• [Team F] +5.5 vs [Team E]
```

**Expected Output for Input 2:**
```
Biggest odds variance:

[Team D] +7.5 vs [Team C]
• FanDuel: +7.5 (-110)
• DraftKings: +9 (-115)
• Variance: 1.5 points
```

**Evaluation Criteria:**
- System successfully filters based on bet parameters
- System identifies variance opportunities across books
- Response provides actionable insights for value bettors

## Implementation Priority

For initial implementation, focus on these three core scenarios:

1. **Sport/Game Browsing** (Scenario 1)
2. **Basic Odds Display** (Scenario 2)
3. **Cross-Book Comparison** (Scenario 3)

These three scenarios cover the fundamental user journey Reagan described: browsing available games, viewing odds for a specific game, and comparing across sportsbooks to find value.

The futures betting scenario (#4) would be an excellent addition if time permits, as Reagan specifically highlighted the value of comparing futures bets.

Advanced filtering (#5) is more of a stretch goal since it requires more complex processing of the API data.

## Evaluation Methodology

When testing these scenarios, evaluate each response on:

1. **Accuracy**: Does the system provide correct odds and information?
2. **Completeness**: Does the response include all necessary information?
3. **Clarity**: Is the information presented in a clear, easy-to-understand format?
4. **Relevance**: Does the response address the user's specific query?
5. **Value-Add**: Does the system provide insights beyond raw data (e.g., identifying best values)?

Document any gaps or issues encountered during testing to inform future improvements.
