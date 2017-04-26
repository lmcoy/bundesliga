
class Team:
    def __init__(self, name):
        self.name = name
        self.home_weights = 0.0
        self.home_goals =  0.0
        self.home_goals_against = 0.0
        self.avg_home_goals = 0.0
        self.avg_home_goals_against = 0.0
        self.away_weights = 0.0
        self.away_goals =  0.0
        self.away_goals_against = 0.0
        self.avg_away_goals = 0.0
        self.avg_away_goals_against = 0.0
        self.points = 0
        self.goals = 0
        self.goals_against = 0

    def AddGameAtHome(self, goals, goals_against, weight):
        self.home_weights += weight
        self.home_goals += goals * weight
        self.home_goals_against += goals_against * weight
        self.avg_home_goals = self.home_goals / self.home_weights
        self.avg_home_goals_against = self.home_goals_against / self.home_weights
        if goals > goals_against:
            self.points += 3
        if goals == goals_against:
            self.points += 1
        self.goals += goals
        self.goals_against += goals_against

    def AddGameAway(self, goals, goals_against, weight):
        self.away_weights += weight
        self.away_goals += goals * weight
        self.away_goals_against += goals_against * weight
        self.avg_away_goals = self.away_goals / self.away_weights
        self.avg_away_goals_against = self.away_goals_against / self.away_weights
        if goals > goals_against:
            self.points += 3
        if goals == goals_against:
            self.points += 1
        self.goals += goals
        self.goals_against += goals_against

    def DefenseStrengthHome(self, avg_goals_away):
        return self.avg_home_goals_against / avg_goals_away

    def DefenseStrengthAway(self, avg_goals_home):
        return self.avg_away_goals_against / avg_goals_home

    def AttackStrengthHome(self, avg_goals_home):
        return self.avg_home_goals / avg_goals_home

    def AttackStrengthAway(self, avg_goals_away):
        return self.avg_away_goals / avg_goals_away
