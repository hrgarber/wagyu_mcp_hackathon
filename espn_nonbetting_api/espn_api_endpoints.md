# ESPN's hidden API endpoints

## Football

### College Football 

**Latest News**: http://site.api.espn.com/apis/site/v2/sports/football/college-football/news

**Latest Scores**: http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard

- query params:

   - calendar: 'blacklist'
   - dates: any date in YYYYMMDD
   
**Game Information**: http://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=:gameId

- params:

   - gameId: identifier of some game (EX: 400934572 for 2017 Army vs Navy)
        
**Team Information**: http://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/:team

- params: 

   - team: some team abbreviation (EX: 'all' for Allegheny, 'gt' for Georgia Tech, 'wisconsin' for Wisconsin)
   
**Rankings**: http://site.api.espn.com/apis/site/v2/sports/football/college-football/rankings

### NFL

**Scores**: http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard

**News**: http://site.api.espn.com/apis/site/v2/sports/football/nfl/news

**All Teams**: http://site.api.espn.com/apis/site/v2/sports/football/nfl/teams

**Specific Team**: http://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/:team


## Baseball

### MLB

**Scores**: http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard

**News**: http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/news

**All Teams**: http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams

**Specific Team**: http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams/:team

### College Baseball

**Scores**: https://site.api.espn.com/apis/site/v2/sports/baseball/college-baseball/scoreboard

## Hockey

**Scores**: http://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard

**News**: http://site.api.espn.com/apis/site/v2/sports/hockey/nhl/news

**All Teams**: http://site.api.espn.com/apis/site/v2/sports/hockey/nhl/teams

**Specific Team**: http://site.api.espn.com/apis/site/v2/sports/hockey/nhl/teams/:team


## Basketball

### NBA

**Scores**: http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard

**News**: http://site.api.espn.com/apis/site/v2/sports/basketball/nba/news

**All Teams**: http://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams

**Specific Team**: http://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/:team


### WNBA

**Scores**: http://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard

**News**: http://site.api.espn.com/apis/site/v2/sports/basketball/wnba/news

**All Teams**: http://site.api.espn.com/apis/site/v2/sports/basketball/wnba/teams

**Specific Team**: http://site.api.espn.com/apis/site/v2/sports/basketball/wnba/teams/:team


### Women's College Basketball

**Scores**: http://site.api.espn.com/apis/site/v2/sports/basketball/womens-college-basketball/scoreboard

**News**: http://site.api.espn.com/apis/site/v2/sports/basketball/womens-college-basketball/news

**All Teams**: http://site.api.espn.com/apis/site/v2/sports/basketball/womens-college-basketball/teams

**Specific Team**: http://site.api.espn.com/apis/site/v2/sports/basketball/womens-college-basketball/teams/:team


### Men's College Basketball

**Scores**: http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard

**News**: http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/news

**All Teams**: http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams

**Specific Team**: http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/:team



## Soccer

**Scores**: http://site.api.espn.com/apis/site/v2/sports/soccer/:league/scoreboard

- params:

   - league: some league abbreviation (EX: 'eng.1' for EPL, 'usa.1' for MLS) 
   
**Latest News**: http://site.api.espn.com/apis/site/v2/sports/soccer/:league/news

**List of Team Information**: http://site.api.espn.com/apis/site/v2/sports/soccer/:league/teams


Will update with more information as I find more...
