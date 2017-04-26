from team import * 

class League:
    def __init__(self, teams):
        self.teams = {}
        for team in teams:
            self.teams[team] = Team(team) 
        self.goal_home = 0
        self.goal_away = 0
        self.n_games = 0
        self.missing = []

    def AddMatch(self, team1, team2, goals1, goals2, weight):
        if not team1 in self.teams:
            raise Exception("error: %s not in league" % team1)
        if not team2 in self.teams:
            raise Exception("error: %s not in league" % team2)
        self.teams[team1].AddGameAtHome(goals1, goals2, weight)
        self.teams[team2].AddGameAway(goals2, goals1, weight)
        self.goal_home += goals1
        self.goal_away += goals2
        self.n_games += 1

    def Print(self):
        avg_goal_home = (float(self.goal_home) / float(self.n_games))
        avg_goal_away = (float(self.goal_away) / float(self.n_games))

        for team in self.teams:
            t = self.teams[team]
            print "%20s %3d   AH: %.1f AA: %.1f DH: %.1f DA: %.1f"  \
                % (t.name, t.points, \
                        t.AttackStrengthHome(avg_goal_home), t.AttackStrengthAway(avg_goal_away), \
                        t.DefenseStrengthHome(avg_goal_away), t.DefenseStrengthAway(avg_goal_home) )
        print "avg goals for home team: %f" % avg_goal_home
        print "avg goals for away team: %f" % avg_goal_away

    def AvgGoalsHome(self):
        return (float(self.goal_home) / float(self.n_games))

    def AvgGoalsAway(self):
        return (float(self.goal_away) / float(self.n_games))

    def AttackStrengthHome(self, team):
        if not team in self.teams:
            raise Exception("unknown team: %s" % team)
        avg_goal_home = (float(self.goal_home) / float(self.n_games))
        t = self.teams[team]
        return t.AttackStrengthHome(avg_goal_home)

    def AttackStrengthAway(self, team):
        if not team in self.teams:
            raise Exception("unknown team: %s" % team)
        avg_goal_away = (float(self.goal_away) / float(self.n_games))
        t = self.teams[team]
        return t.AttackStrengthAway(avg_goal_away)

    def DefenseStrengthHome(self, team):
        if not team in self.teams:
            raise Exception("unknown team: %s" % team)
        avg_goal_away = (float(self.goal_away) / float(self.n_games))
        t = self.teams[team]
        return t.DefenseStrengthHome(avg_goal_away)

    def DefenseStrengthAway(self, team):
        if not team in self.teams:
            raise Exception("unknown team: %s" % team)
        avg_goal_home = (float(self.goal_home) / float(self.n_games))
        t = self.teams[team]
        return t.DefenseStrengthAway(avg_goal_home)

    def AddMissingMatch(self, team1, team2):
        self.missing.append( (team1, team2) )

    def GetList(self):
        l = []
        for team in self.teams:
            l.append( (self.teams[team].name, self.teams[team].points) )
        return sorted(l, key=lambda x: x[1], reverse=True)

    def GetTeams(self):
        return list(self.teams.keys())

    def GetAvgGoals(self, team1, team2):
        avg_goals1 = self.AvgGoalsHome() 
        avg_goals2 = self.AvgGoalsAway() 
        ah = self.AttackStrengthHome(team1)
        da = self.DefenseStrengthAway(team2)
        aa = self.AttackStrengthAway(team2)
        dh = self.DefenseStrengthHome(team1)
        goals1 = avg_goals1 * ah * da
        goals2 = avg_goals2 * aa * dh
        return (goals1, goals2)
