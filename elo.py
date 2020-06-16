import pandas as pd
import csv
import datetime
import schedule
import time

k = 40
h = 100

def elo_diff(ratings, teams, game):
    global h
    return (ratings[teams[game.h_team]] + h) - ratings[teams[game.a_team]]

def w_pct(ratings, teams, game):
    return 1 / (10 ** (-elo_diff(ratings, teams, game) / 400) + 1)

def update_elo(ratings, teams, game):
    global k
    diff = elo_diff(ratings, teams, game)
    if game.diff > 0:
        win = 1
    else:
        diff *= -1
        win = 0
    margin_mult = ((abs(game.diff) + 3) ** 0.8) / (0.006 * diff + 7.5)
    new = margin_mult * k * (win - w_pct(ratings, teams, game))
    ratings[teams[game.h_team]] += new
    ratings[teams[game.a_team]] -= new

def simulate(end_yr, initial):
    ratings = [initial]
    games, teams = schedule.season_schedule(end_yr)
    for date in games:
        new_ratings = ratings[-1].copy()
        for game in games[date]:
            update_elo(new_ratings, teams, game)
        ratings.append(new_ratings)
    return games, teams, ratings

def output(games, teams, ratings, graph=False):
    with open('output.csv', mode='w') as f:
        w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Date'] + list(teams.keys()))
        dates = list(games.keys())
        for i in range(len(dates)):
            row = [str(dates[i])] + ratings[i]
            w.writerow(row)
    if graph:
        title = '{}-{} NBA Season'.format(dates[0].year, str(dates[0].year + 1)[2:])
        pd.options.plotting.backend = 'plotly'
        df = pd.read_csv('output.csv', index_col='Date')
        df.columns.name = 'Team'
        fig = df.plot.line(title='2011-12 NBA Season', facet_col='Team', facet_col_wrap=5)
        fig.show()

_,_,prev = simulate(2011, [1500]*30)
after = [(3*x + 1*y)/4 for x,y in zip(prev[-1],[1500]*30)]
output(*simulate(2012, after), graph=True)