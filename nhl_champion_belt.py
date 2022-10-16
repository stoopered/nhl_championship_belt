import requests
import pandas
from datetime import date

class Team:
  def __init__(self, id, name, home=False, score=0):
    self.id = id
    self.name = name
    self.home = home
    self.score = score

def id_lookup(tname):
    api_url = "https://statsapi.web.nhl.com/api/v1/teams"
    response = requests.get(api_url)
    teams = response.json()['teams']
    for i in teams:
        if i['name'] == tname:
            team = Team(i['id'],i['name'])
            break
    return team

tname = 'Colorado Avalanche'
current_champ_team = id_lookup(tname)
startofseason = '2022-10-07'
today = date.today()
daterange = pandas.date_range(startofseason,today,freq='d').strftime('%Y-%m-%d').tolist()

id = id_lookup(tname)
for date in daterange:

    print(f'{date} -- Current Champion {current_champ_team.name}')
    api_url = f"https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.linescore&teamId={current_champ_team.id}&date={date}&gameType=R"
    response = requests.get(api_url)
    game = response.json()
    if len(game['dates']) == 0:
        print(f'Did not play on {date}')
    else:
        home_team = game['dates'][0]['games'][0]['teams']['home']['team']['name']
        away_team = game['dates'][0]['games'][0]['teams']['away']['team']['name']
        if home_team == current_champ_team.name:
            current_champ_team.home = True
            current_champ_team.score = game['dates'][0]['games'][0]['teams']['home']['score']
            comp_team = Team(game['dates'][0]['games'][0]['teams']['away']['team']['id'],game['dates'][0]['games'][0]['teams']['away']['team']['name'],False,game['dates'][0]['games'][0]['teams']['away']['score'])
            if (comp_team.score > current_champ_team.score):
                print(f'{current_champ_team.name} defeated by {comp_team.name}')
                current_champ_team = id_lookup(comp_team.name)
            else:
                print(f'{current_champ_team.name} wins against {comp_team.name}')
        else:
            current_champ_team.score = game['dates'][0]['games'][0]['teams']['away']['score']
            comp_team = Team(game['dates'][0]['games'][0]['teams']['home']['team']['id'],game['dates'][0]['games'][0]['teams']['home']['team']['name'],False,game['dates'][0]['games'][0]['teams']['home']['score'])
            if (comp_team.score > current_champ_team.score):
                print(f'{current_champ_team.name} defeated by {comp_team.name}')
                current_champ_team = id_lookup(comp_team.name)
            else:
                print(f'{current_champ_team.name} wins against {comp_team.name}')

 