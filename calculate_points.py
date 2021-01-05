import requests
import json
import subprocess

points = {}


def run(*args):
  return subprocess.check_call(['git'] + list(args))

def commit():
  run("add",".")
  run("commit", "-am", "Updated scores")
  run("push")

def  fetch():
  url = "https://dev132-cricket-live-scores-v1.p.rapidapi.com/scorecards.php?seriesid=2679&matchid=48825"
  payload = {}
  headers = {
    'x-rapidapi-key': 'dd8d46530cmsh63fc0c06dd092f1p1ca8a6jsn143ccf9a171f',
    'x-rapidapi-host': 'dev132-cricket-live-scores-v1.p.rapidapi.com'
  }
  response = requests.request("GET", url, headers=headers, data = payload)
  return response.json()

def calc_batsman_score(data):
  score = 0
  run = data['runs']
  if run:
    run = int(run)
    score = run
    if run >= 50:
      score += 5
    if run >= 100:
      score += 5
  return score

def calc_bowler_score(data):
  score = 0
  wickets = data['wickets']
  if wickets:
    wickets = int(wickets)
    score = wickets * 15
    if wickets >= 5:
      score += 10
  return score

def parse_how_out(how_out):
  for data in how_out:
    score = 5
    player = ""
    if data[0: 2] == 'c:':
      player = data[3:].split(' ')[0]
    elif data[0:3] == 'c&b':
      player = data[5:]
    elif data[0:7] == 'run out':
      player = data[9:-1]
    elif data[0: 2] == 'st':
      player = data[4:].split(' ')[0]
    if player != "" and player in points:
      points[player] = points[player] + score
    else:
      points[player] = score


if __name__ == "__main__":
  print("Executing")
  data=fetch()
  innings = data['fullScorecard']['innings']
  points = {}
  how_out = []
  for inning in innings:
    for batsman in inning['batsmen']:
      player = batsman['name'].split(" ")[-1]
      score = calc_batsman_score(batsman)
      points[player] = score
      how_out.append(batsman['howOut'])
    for bowler in inning['bowlers']:
      player = bowler['name'].split(" ")[-1]
      score = calc_bowler_score(bowler)
      if player in points:
        points[player] = points[player] + score
      else:
        points[player] = score

  parse_how_out(how_out)
  points = json.dumps(points)

  with open("points.json", "w") as file1:
    file1.write(points)
  commit()