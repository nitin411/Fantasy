import requests
import json
import subprocess

def run(*args):
  return subprocess.check_call(['git'] + list(args))

def commit():
  try:
    run("pull")
    run("add",".")
    run("commit", "-am", "Updated scores")
    run("push")
  except Exception as e:
    print("Exception")
def  fetch():
  url = "https://dev132-cricket-live-scores-v1.p.rapidapi.com/scorecards.php?seriesid=2603&matchid=48442"
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
  print(str(data))
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


if __name__ == "__main__":
  print("Executing")
  data=fetch()
  innings = data['fullScorecard']['innings']
  points = {"Rahane": 0, "Ashwin": 0, "Bumrah": 0, "Jadeja": 0, "Pujara": 0, "Sharma": 0, "Labuschagne": 0, "Smith": 0, "Warner": 0, "Agarwal": 0, "Yadav": 0, "Pant": 0, "Rahul": 0, "Cummins": 0, "Green": 0, "Hazlewood": 0, "Head": 0, "Lyon": 0, "Pattinson": 0, "Starc": 0, "Siraj": 0, "Natarajan": 0, "Saha": 0, "Saini": 0, "Shaw": 0, "Gill": 0, "Thakur": 0, "Vihari": 0, "Paine": 0, "Henriques": 0, "Neser": 0, "Pucovski": 0, "Swepson": 0, "Wade": 0, "Abbott": 0}
  how_out = []
  scores = {}
  for inning in innings:

    team = inning['team']['shortName']
    if team in scores: 
      if(inning['isDeclared']=="true"):
        scores[team]+=" and " + inning['run'] + "/" + inning['wicket'] + " dec."
      else:
        scores[team]+=" and " + inning['run'] + "/" + inning['wicket']
    else:
      if(inning['isDeclared']=="true"):
        scores[team]=inning['run'] + "/" + inning['wicket'] + " dec."
      else:
        scores[team]=inning['run'] + "/" + inning['wicket']
    for batsman in inning['batsmen']:
      player = batsman['name'].split(" ")[-1]
      score = calc_batsman_score(batsman)
      points[player] = points[player] + score
      how_out.append(batsman['howOut'])
    for bowler in inning['bowlers']:
      player = bowler['name'].split(" ")[-1]
      score = calc_bowler_score(bowler)
      if player in points:
        points[player] = points[player] + score
      else:
        points[player] = score
      print("Bowling after " + str(player) + str(points[player]))

  parse_how_out(how_out)
  points = json.dumps(points)
  with open("points.json", "w") as file1:
    file1.write("data = '")
    file1.write(points)
    file1.write("'")
  
  team1Score=""
  team2Score=""
  j=0
  for i in scores: 
    if (j == 0): 
      team1 = i
      team1Score = scores[i]
    else:
      team2 = i
      team2Score = scores[i]      
    j = j + 1

  with open("scoreboard.json", "w") as file:
    file.write("scoreboard = '")
    file.write("{\"match\": 3,")
    file.write("\"location\":\"Sydney\",")
    file.write("\"scoreBreakUp\": [{\"batting\": \"" + team1 + "\"," + "\"score\": \"" + team1Score + "\"},")
    file.write("{\"batting\": \"" + team2 + "\"," + "\"score\": \"" + team2Score + "\"}],")
    file.write("\"overs\": \"" + data['fullScorecard']['innings'][0]['over'] + "\"}'")
  commit()
