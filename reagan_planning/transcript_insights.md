# Sports Betting AI - Transcript Insights

This document summarizes key insights from the conversation with Reagan about sports betting user needs and preferences.

## 1. User Stories / Scenarios

### Scenario 1: The Value Shopper
**User Need:** "I want to place a bet on Loyola Marymount at the highest possible odds"  
**Action:** Compares odds across multiple sportsbooks for a specific selection  
**Output Example:** "DraftKings offers Loyola Marymount at +925, while FanDuel has them at +900"

### Scenario 2: The Casual Game Night Better
**User Need:** "I'm watching the Lakers game with friends and want to place a quick bet"  
**Action:** Looks up basic odds for a specific game  
**Output Example:** "Lakers vs. Grizzlies: Lakers -4.5, O/U 224.5, Lakers ML -190"

### Scenario 3: The Trend Spotter
**User Need:** "I want to see if there's unusual line movement on any games tonight"  
**Action:** Looks for significant recent changes in betting lines  
**Output Example:** "The White Sox line has moved from +300 to +375 in the last hour despite 60% of bets being placed on them"

## 2. Data Points to Track

| Data Category | Priority | Examples |
|---------------|----------|----------|
| Basic Odds | High | Spread, Money Line, Over/Under |
| Book Comparison | High | Same bet across multiple sportsbooks |
| Line Movement | Medium | Changes from opening line to current |
| Bet Distribution | Medium | % of bets vs % of money on each side |
| Futures | Medium | Long-term bets with higher variation across books |

## 3. User Experience Flow

1. **Initial Query**
   - User asks: "Show me the line for Lakers-Grizzlies"
   
2. **Primary Response**
   - Default sportsbook odds (Caesar's suggested)
   - Standard format: Spread, O/U, Money Line
   
3. **Secondary Options**
   - "Would you like to see odds from other sportsbooks?"
   - "Would you like to see betting trends for this game?"
   
4. **Advanced Data (On Request)**
   - Line movement information
   - Bet distribution (money vs. bets)

## 4. Implementation Priorities

1. Basic odds retrieval for major US sports (single sportsbook)
2. Multiple sportsbook comparison for same game/bet
3. Format optimization for AI chat interface
4. Line movement indicators (if time permits)
5. Bet distribution data (if available in your API)

## 5. Key Insights from Reagan

- **Futures bets** have the most variation between sportsbooks and offer the best opportunity for value shopping
- **Line movement** is a key indicator that bettors look for to identify potential value
- **Bet distribution** (% of money vs. % of bets) can signal "sharp" money and is valuable information
- **Layered information** is important - start with basic odds, then offer more detailed information
- **User preferences** for which sportsbooks to display is important
- **Anomalies** in odds or betting patterns can either attract or repel bettors depending on their strategy
- **Default display** should be simple (spread, money line, over/under) with options to see more
