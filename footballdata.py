import urllib2
import json
import os
from league import *

class Error(Exception):
    pass

class DownloadError(Error):
    def __init__(self, msg):
        self.msg = msg

def download_leagues(year):
    url = "http://api.football-data.org/v1/competitions/?season=%d" % year 
    download(url, "leagues_%d.json" % year)

def download_teams(league_id):
    url = "http://api.football-data.org/v1/competitions/%d/teams" % league_id
    download(url, "teams_%d.json" % league_id)

def download_matches(league_id):
    url = "http://api.football-data.org/v1/competitions/%d/fixtures" % league_id
    download(url, "matches_%d.json" % league_id)

def download(url, fout):
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        raise DownloadError(str(e.reason))
    with open(fout, 'w') as output:
        output.write(response.read())

def update_league_ids(year, download):
    if os.path.exists("leagues_%d.json"):
        with open("leagues_%d.json" % year) as infile:
            data = json.load(infile)
    else:
        download_league_ids(year)

def LoadLeagues(year, update=False):
    if update or not os.path.exists("leagues_%d.json" % year):
        download_leagues(year)
    with open('leagues_%d.json' % year) as infile:
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
    leagues = LoadLeagues(year, update)
    league_id = None
    for league in leagues:
        if league["league"] == name:
            league_id = league["id"]
    if league_id == None:
        raise Exception("unknown league")
    teams = LoadTeams(league_id, update)

    data = LoadGames(league_id, update)
    
    timestamp = os.path.getmtime("leagues_%d.json" % year)
    league = League(teams, unixtime=timestamp)
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
