import urllib2
import json
import os
from league import *

def download_leagues():
    url = "http://api.football-data.org/v1/competitions/" 
    download(url, "leagues.json")

def download_teams(league_id):
    url = "http://api.football-data.org/v1/competitions/%d/teams" % league_id
    download(url, "teams_%d.json" % league_id)

def download_matches(league_id):
    url = "http://api.football-data.org/v1/competitions/%d/fixtures" % league_id
    download(url, "matches_%d.json" % league_id)

def download(url, fout):
    response = urllib2.urlopen(url)
    with open(fout, 'w') as output:
        output.write(response.read())

def update_league_ids(year, download):
    if os.path.exists("leagues_%d.json"):
        with open("leagues_%d.json" % year) as infile:
            data = json.load(infile)
    else:
        download_league_ids(year)

def LoadLeagues(update=False):
    if update or not os.path.exists("leagues.json"):
        download_leagues()
    with open('leagues.json') as infile:
        data = json.load(infile)
    return data

def LoadTeams(league_id, update=False):
    if update or not os.path.exists("teams_%d.json" % league_id):
        download_teams(league_id)
    with open("teams_%d.json" % league_id) as infile:
        data = json.load(infile)
    teams = []
    for team in data["teams"]:
        teams.append( team["name"] )

    return teams

def LoadGames(league_id, update=False):
    if update or not os.path.exists("matches_%d.json" % league_id):
        download_matches(league_id)
    with open("matches_%d.json" % league_id) as infile:
        data = json.load(infile)
    return data

def New(name, year, matchdays, update=False):
    leagues = LoadLeagues(update)
    league_id = None
    for league in leagues:
        if league["league"] == name:
            league_id = league["id"]
    if league_id == None:
        raise Exception("unknown league")
    teams = LoadTeams(league_id, update)

    data = LoadGames(league_id, update)
    
    league = League(teams)
    for f in data["fixtures"]:
        team1 = f["homeTeamName"]
        team2 = f["awayTeamName"]
        goals1 = f["result"]["goalsHomeTeam"]
        goals2 = f["result"]["goalsAwayTeam"]
        matchday = f["matchday"]
        weight = 1.0
        if matchday in matchdays:
            if goals1 != None and goals2 != None:
                league.AddMatch(team1, team2, goals1, goals2, weight)
            else:
                league.AddMissingMatch(team1, team2)
        else:
            league.AddMissingMatch(team1, team2)

    return league
