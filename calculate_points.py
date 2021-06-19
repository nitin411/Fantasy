import requests
import json
import subprocess

players = ["Ajinkya Rahane",
"Cheteshwar Pujara",
"Kane Williamson",
"Ravichandran Ashwin",
"Ravindra Jadeja",
"Rohit Sharma",
"Ross Taylor",
"Tim Southee",
"Trent Boult",
"Virat Kohli",
"Henry Nicholls",
"Ishant Sharma",
"Jasprit Bumrah",
"Kyle Jamieson",
"Matt Henry",
"Mohammed Shami",
"Neil Wagner",
"Rishabh Pant",
"Shubman Gill",
"Tom Latham",
"Ajaz Patel",
"BJ Watling",
"Colin de Grandhomme",
"Devon Conway",
"Hanuma Vihari",
"Mohammed Siraj",
"Tom Blundell",
"Umesh Yadav",
"Will Young",
"Wriddhiman Saha"]


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
  url = "https://dev132-cricket-live-scores-v1.p.rapidapi.com/scorecards.php?seriesid=2781&matchid=50883"
  payload = {}
  headers = {
    'x-rapidapi-key': 'dd8d46530cmsh63fc0c06dd092f1p1ca8a6jsn143ccf9a171f',
    'x-rapidapi-host': 'dev132-cricket-live-scores-v1.p.rapidapi.com'
  }
  response = requests.request("GET", url, headers=headers, data = payload)
  print(response.json())
  return response.json()

def calc_batsman_score(data):
  score = 0
  bonus = 0
  run = data['runs']
  if run:
    run = int(run)
    score = run
    if run >= 50:
      bonus += 5
    if run >= 100:
      bonus += 5
  return (score, bonus)

def calc_bowler_score(data):
  score = 0
  bonus = 0
  wickets = data['wickets']
  if wickets:
    wickets = int(wickets)
    score = wickets * 15
    if wickets >= 4:
      bonus += 5
    if wickets >= 5:
      bonus += 5
  return (score, bonus)


def get_full_name(nick_name):
  for player in players:
    player_lower_case = player.lower()
    if nick_name == player_lower_case.split(' ')[1]:
      return player_lower_case


def parse_how_out(how_out):
  for data in how_out:
    score = 10
    player = ""
    if data[0: 2] == 'c:':
      player = data[3:].split(' ')[0]
      score = 5
    elif data[0:3] == 'c&b':
      player = data[5:]
      score = 5
    elif data[0:7] == 'run out':
      player = data[9:-1]
    elif data[0: 2] == 'st':
      player = data[4:].split(' ')[0]
    player = player.lower()
    player = get_full_name(player)
    if player != "" and player in points:
      points[player]["score"] = points[player]["score"] + score


if __name__ == "__main__":
  print("Executing")
 # commit()
  data=fetch()
  innings = data['fullScorecard']['innings']
  points = {}
  for player in players:
    points[player.lower()] = {
      "score": 0,
      "bonus": 0
    }
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
      player = batsman['name'].lower()
      score = calc_batsman_score(batsman)
      print(score)
      points[player]["score"] = points[player]["score"] + score[0]
      points[player]["bonus"] = points[player]["bonus"] + score[1]
      how_out.append(batsman['howOut'])
    for bowler in inning['bowlers']:
      player = bowler['name'].lower()
      score = calc_bowler_score(bowler)
      print(score)
      if player in points:
        points[player]["score"] = points[player]["score"] + score[0]
        points[player]["bonus"] = points[player]["bonus"] + score[1]
      else:
        points[player]["score"] = score
      print("Bowling after " + str(player) + str(points[player]))


  
  parse_how_out(how_out)

  points["rishab pant"] = points["rishabh pant"]

  points = json.dumps(points)
  with open("points.json", "w") as file1:
    file1.write("data = '")
    file1.write(points)
    file1.write("'")
  
  team1Score="0/0"
  team2Score="0/0"
  team1="IND"
  team2="NZ"
  j=0
  print(scores)
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
    file.write("{\"day\": 1,")
    file.write("\"location\":\"Southampton\",")
    file.write("\"scoreBreakUp\": [{\"batting\": \"" + team1 + "\"," + "\"score\": \"" + team1Score + "\"},")
    file.write("{\"batting\": \"" + team2+ "\"," + "\"score\": \"" + team2Score + "\"}],")
    file.write("\"overs\": \"" + data['fullScorecard']['innings'][0]['over'] + "\"}'")
  commit()
