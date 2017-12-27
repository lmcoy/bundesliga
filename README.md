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

Example
-------

Prediction for Bundesliga season 17/18 based on the first 17 matches. The columns show the 
probability in percents that a team finishes in the position in the final table.

prob in %                |     1 |      2 |      3 |      4 |      5 |      6 |      7 |      8 |      9 |     10 |     11 |     12 |     13 |     14 |     15 |     16 |     17 |     18| avg. pts
-------------------------|-------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|-------|---------
FC Bayern München        | 99.60 |   0.32 |   0.08 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00|  79
Borussia Dortmund        |  0.20 |  47.80 |  24.84 |  12.68 |   5.68 |   4.84 |   1.80 |   1.24 |   0.68 |   0.08 |   0.16 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00|  61
Bayer Leverkusen         |  0.08 |  25.32 |  25.44 |  17.84 |  11.96 |   7.76 |   4.92 |   2.88 |   1.72 |   1.16 |   0.84 |   0.04 |   0.04 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00|  58
FC Schalke 04            |  0.08 |  12.96 |  20.24 |  18.96 |  15.28 |  10.72 |   8.56 |   5.56 |   4.00 |   2.32 |   0.92 |   0.36 |   0.04 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00|  56
TSG 1899 Hoffenheim      |  0.00 |   4.00 |   7.04 |  13.64 |  15.76 |  14.56 |  12.72 |  11.08 |   9.68 |   6.32 |   3.68 |   1.12 |   0.28 |   0.08 |   0.04 |   0.00 |   0.00 |   0.00|  53
Red Bull Leipzig         |  0.00 |   3.60 |   7.64 |  11.04 |  13.72 |  13.48 |  13.68 |  11.00 |  10.04 |   7.76 |   5.08 |   2.36 |   0.44 |   0.16 |   0.00 |   0.00 |   0.00 |   0.00|  52
Eintracht Frankfurt      |  0.00 |   2.24 |   4.52 |   7.76 |  10.84 |  11.92 |  14.24 |  13.04 |  12.52 |  10.48 |   6.76 |   3.88 |   1.36 |   0.40 |   0.04 |   0.00 |   0.00 |   0.00|  51
Bor. Mönchengladbach     |  0.00 |   1.44 |   3.84 |   6.16 |   9.68 |  11.28 |  13.44 |  13.08 |  13.28 |  11.84 |   9.36 |   5.12 |   1.00 |   0.36 |   0.12 |   0.00 |   0.00 |   0.00|  50
FC Augsburg              |  0.04 |   1.36 |   3.76 |   6.56 |   7.88 |   9.96 |  12.88 |  14.88 |  13.36 |  12.04 |  10.16 |   4.64 |   1.56 |   0.56 |   0.24 |   0.12 |   0.00 |   0.00|  49
Hertha BSC               |  0.00 |   0.60 |   1.80 |   3.48 |   5.92 |   8.88 |   8.16 |  13.04 |  14.72 |  17.00 |  13.64 |   8.92 |   2.44 |   0.92 |   0.36 |   0.12 |   0.00 |   0.00|  48
Hannover 96              |  0.00 |   0.36 |   0.72 |   1.80 |   3.00 |   5.32 |   7.24 |  10.08 |  13.56 |  17.72 |  20.12 |  12.32 |   4.32 |   2.40 |   0.80 |   0.12 |   0.12 |   0.00|  46
VfL Wolfsburg            |  0.00 |   0.00 |   0.08 |   0.08 |   0.24 |   1.24 |   2.08 |   3.40 |   4.52 |   8.76 |  15.96 |  27.60 |  16.04 |   9.60 |   6.20 |   2.96 |   1.24 |   0.00|  41
VfB Stuttgart            |  0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.04 |   0.36 |   0.48 |   1.40 |   4.48 |  11.64 |  22.84 |  22.44 |  18.36 |  11.64 |   6.20 |   0.12|  36
FSV Mainz 05             |  0.00 |   0.00 |   0.00 |   0.00 |   0.04 |   0.00 |   0.16 |   0.28 |   0.72 |   1.56 |   3.52 |   7.80 |  19.92 |  20.00 |  17.92 |  16.52 |  11.48 |   0.08|  35
SC Freiburg              |  0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.04 |   0.04 |   0.08 |   0.52 |   0.88 |   3.84 |   7.76 |  15.08 |  20.44 |  21.60 |  18.28 |  11.24 |   0.20|  35
Hamburger SV             |  0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.08 |   0.36 |   0.88 |   3.48 |   6.92 |  11.76 |  16.36 |  24.88 |  35.04 |   0.24|  31
Werder Bremen            |  0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.04 |   0.00 |   0.12 |   0.32 |   0.60 |   2.96 |   7.72 |  10.88 |  17.92 |  25.16 |  33.68 |   0.60|  31
FC Köln                  |  0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.00 |   0.04 |   0.20 |   1.00 |  98.76|  15
