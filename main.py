import copy
import numpy
import footballdata
from scipy import special
import math

    
def PrintRanking(league):
    ranking = league.GetList() 
    for i in range(0, len(ranking)):
        print "%2d %-30s %3d" % (i+1, ranking[i][0], ranking[i][1])


def SimulateSeason(refleague, newleague):
    nleague = copy.deepcopy(newleague)
    avg_goals1 = refleague.AvgGoalsHome() 
    avg_goals2 = refleague.AvgGoalsAway() 
    for match in nleague.missing:    
        ah = refleague.AttackStrengthHome(match[0])
        da = refleague.DefenseStrengthAway(match[1])
        aa = refleague.AttackStrengthAway(match[1])
        dh = refleague.DefenseStrengthHome(match[0])
        goals1 = numpy.random.poisson(lam=avg_goals1 * ah * da)
        goals2 = numpy.random.poisson(lam=avg_goals2 * aa * dh)
        team1 = match[0]
        team2 = match[1]
        nleague.AddMatch(team1, team2, goals1, goals2, 1.0)
    return nleague

def SimulateSeason2(refleague, newleague):
    nleague = copy.deepcopy(newleague)
    for match in nleague.missing:    
        goals = refleague.GetAvgGoals(match[0], match[1])
        goals1 = numpy.random.poisson(lam=goals[0])
        goals2 = numpy.random.poisson(lam=goals[1])
        team1 = match[0]
        team2 = match[1]
        nleague.AddMatch(team1, team2, goals1, goals2, 1.0)
    return nleague

def SimulateCurrent(league, nleague):
    data = {}
    table = league.GetList()
    for team in table:
        data[team[0]] = [0]*18

    N = 1000
    for i in xrange(0,N):
        league_end = SimulateSeason(league, nleague)
        table_end = league_end.GetList()
        for pos in xrange(0,len(table_end)):
            name = table_end[pos][0]
            data[name][pos] += 1

    print "%-24s |%s" % ("prob in %", "  ".join( "%6d" % x for x in xrange(1,len(table)+1)))
    print "-"*168
    for team in data:
        matches = ", ".join( "%6.2f" % (float(x)/float(N)*100.0) for x in data[team])
        print "%-24s |%s" % (team, matches)
    

def winning_chances(goals1, goals2):
# skellam distribution
    p = lambda k: math.exp(-(goals1+goals2))\
            *(goals1/goals2)**(float(k)/2.0)\
            *special.iv(math.fabs(float(k)), 2.0*math.sqrt(goals1*goals2))
    p1 = 0.0
    p2 = 0.0
    for i in xrange(1, 15):
        p1 += p(i)
        p2 += p(-i)
    return (p1*100.0, 100.*p(0), 100.*p2)


if __name__ == "__main__":
    print 'load reference league to calculate team strength'
    league = footballdata.New("BL1", 2016, [x for x in xrange(1,35)])
    print "played matches: %d" % (league.n_games/(len(league.teams)/2))
    PrintRanking(league)

    while True:
        c = raw_input('> ')
        if c == "exit":
            exit(0)
        elif c == "table":
            PrintRanking(league)
        elif c == "simseason":
            nleague = footballdata.New("BL1", 2016, [])
            end = SimulateSeason(league, nleague)
            PrintRanking(end)
        elif c == "match":
            teams = league.GetTeams()
            for i in range(0,len(teams)):
                print "%2d   %s" % (i, teams[i])
            try:
                team1_i = int(raw_input('team1> '))
                if team1_i < 0 or team1_i >= len(teams):
                    raise Exception("invalid id")
                team2_i = int(raw_input('team2> '))
                if team2_i < 0 or team2_i >= len(teams):
                    raise Exception("invalid id")
            except:
                print 'error'
                continue
            team1 = teams[team1_i]
            team2 = teams[team2_i]
            goals = league.GetAvgGoals(team1, team2)
            print "%s - %s:   %.1f : %.1f" % (team1, team2, goals[0], goals[1])
            c = winning_chances(goals[0], goals[1])
            print "  chance of winning:"
            print "     %s: %.1f%%" % (team1, c[0])
            print "     %s: %.1f%%" % (team2, c[2])
            print "     draw: %.1f%%" %  c[1]
        elif c == "sim":
            SimulateCurrent(league, league)
        elif c == "simfull":
            nleague = footballdata.New("BL1", 2016, [])
            SimulateCurrent(league, nleague)
        elif c == "update":
            league = footballdata.New("BL1", 2016, [x for x in xrange(1,35)], update=True)
        else:
            print "%-15s %s" % ("update", "update data") 
            print "%-15s %s" % ("sim", "get prob." \
                    "for places in standing (use results of played matches)")
            print "%-15s %s" % ("simfull", "get prob. for places in standing"\
                    " (start simulation with 1st match)")
            print "%-15s %s" % ("table", "current table")
            print "%-15s %s" % ("simseason", "simulate the season")
            print "%-15s %s" % ("match", "data for one match")
            print "%-15s %s" % ("exit", "exit")
    






