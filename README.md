Simulate Bundesliga
===================

Simulate the Bundesliga table based on previous matches.

usage: `python main.py` and press enter to see all available commands.

Model
-----

The assumption is that the number of goals which a team scores is poisson distributed.
The mean of the poisson distribution for scored goals of a team depends on the 
offensive strength of the team, the defensive strength of the opponent and whether 
it is a game at home or not.
To get an estimate for the mean of the poisson distribution for goals scored by the 
home team, we use the average of all scored goals in the league so far. The same 
is done for goals scored by the away team.
This obviously does not take the individual offensive and defensive strength of a 
team into account. Hence, we use the factor

    s_i = avg_scored_i / avg_scored
    
as _offensive team strength_ at home (away),
where `avg_scored_i` is the average of scored goals at home (away) by team `i` and
`avg_scored` is the average of scored goals at home (away) of the league.
As _defensive team strength_ at home (away) we use

    d_i = avg_against_i / avg_scored,

where `avg_against_i` is the average of scored goals at home (away) against team `i` and
`avg_scored` is the average of scored goals away (at home) of the league.
For a match of team `i` against team `j`, we use 

    lambda_i = s_i(home) * d_j(away) * avg_scored(home)

as mean of the poisson distribution for goals by team `i` and

    lambda_j = s_j(away) * d_i(home) * avg_scored(away)

as mean for goals by team `j`.
To obtain the chances of a team to finish the league in a certain position in the ranking,
we simulate all remaining games of the league 10,000 times.
Note, that we can only hope that this method is sound, if the first half of the season is
already over.
