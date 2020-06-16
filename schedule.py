from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import os.path
import csv
import string
import datetime

class Game:
    def __init__(self, date, h_team, h_score, a_team, a_score):
        self.date = date
        self.h_team = h_team
        self.a_team = a_team
        self.h_score = h_score
        self.a_score = a_score
        self.diff = h_score - a_score

    def __str__(self):
        return '{} @ {}, {}'.format(self.a_team, self.h_team, self.date)
                
    def __repr__(self):
        return str(self)

def new_schedule_csv(end_yr, path):
    client.season_schedule(season_end_year=end_yr, output_type=OutputType.CSV, output_file_path=path)

def season_schedule(end_yr):
    teams = []
    schedule = {}
    path = './schedules/{}-{}_schedule.csv'.format(end_yr-1, str(end_yr)[-2:])
    if not os.path.isfile(path):
        new_schedule_csv(end_yr, path)
    with open(path, 'r') as csvfile:
        r = csv.reader(csvfile)
        next(r)
        for row in r:
            date = datetime.date(*list(map(int, row[0][:10].split('-'))))
            home_team = string.capwords(row[1])
            away_team = string.capwords(row[3])
            if home_team not in teams:
                teams.append(home_team)
            game = Game(date, home_team, int(row[2]), away_team, int(row[4]))
            if date not in list(schedule.keys()):
                schedule[date] = [game]
            else:
                schedule[date].append(game)
    team_map = {}
    for team in teams:
        team_map[team] = teams.index(team)
    return schedule, team_map