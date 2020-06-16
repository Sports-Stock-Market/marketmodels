import numpy as np
import csv
import datetime
import schedule

games, teams = schedule.season_schedule(2012)
M = np.zeros((30,30))
p = np.zeros(30)
ratings = []
for date in games:
    for game in games[date]:
        M[teams[game.h_team], teams[game.h_team]] += 1
        M[teams[game.a_team], teams[game.a_team]] += 1
        M[teams[game.h_team], teams[game.a_team]] -= 1
        M[teams[game.a_team], teams[game.h_team]] -= 1
        p[teams[game.h_team]] += game.diff
        p[teams[game.a_team]] -= game.diff
    fix_M = np.copy(M) + np.identity(30)
    # fix_p = np.copy(p)
    # fix_M[-1] = np.ones(30)
    # fix_p[-1] = 0
    if np.linalg.det(fix_M) != 0:
        ratings.append(np.linalg.solve(fix_M, p).tolist())

with open('output.csv', mode='w') as f:
    w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    w.writerow(['Date'] + list(teams.keys()))
    dates = list(games.keys())[4:]
    for i in range(len(dates)):
        row = [str(dates[i])] + ratings[i]
        w.writerow(row)