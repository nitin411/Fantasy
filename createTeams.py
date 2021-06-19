import requests
import json
import subprocess
import pandas as pd
import numpy
import itertools

teams = '[{"teamName": "Swagglers","player1": "Rahul","player2": "Paurush","team1": ["Rahane","Warner","Rohit","Bumrah"],"team2": ["Rahane","Warner","Rohit","Bumrah"],"team1Captain": "Bumrah","team2Captain": "Bumrah","team1ViceCaptain": "Rohit","team2ViceCaptain": "Rohit"},{"teamName": "Dhaakads","player1": "Utkarsh","player2": "Abhishek","team1": ["Rahane","Warner","Rohit","Bumrah"],"team2": ["Rahane","Warner","Rohit","Bumrah"],"team1Captain": "Bumrah","team2Captain": "Bumrah","team1ViceCaptain": "Rohit","team2ViceCaptain": "Rohit"}]';

class teams:
  teamName = ""
  player1 = ""
  player2 = ""
  team1 = ""
  team2 = ""
  team1Captain = ""
  team1ViceCaptain = ""
  team2Captain = ""
  team2ViceCaptain = ""
   
  def __init__(self, teamName, player1, team1, team1Captain, team1ViceCaptain):
    self.teamName = teamName
    self.player1 = player1 
    self.team1 = team1
    self.team1Captain = team1Captain
    self.team1ViceCaptain = team1ViceCaptain

  def setPlayer2(self, player2, team2, team2Captain, team2ViceCaptain):
    self.player2 = player2 
    self.team2 = team2
    self.team2Captain = team2Captain
    self.team2ViceCaptain = team2ViceCaptain

  def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

def getPlayersWithLastNamesAndLowerCase(playersList): 
  players = playersList.split(',')
  players = numpy.char.strip(players)
  return [i.lower() for i in players]

def writeTeams(teamNameToFullTeamDict, file1):
  teamsList = []
  for team in teamNameToFullTeamDict:
    teamsList.append(teamNameToFullTeamDict[team])
  json_string = json.dumps([ob.__dict__ for ob in teamsList])
  file1.write(json_string)

def set_teams_in_db(teams):
  url = "https://clash11.herokuapp.com/setteams"
  # teams = [
  #   {
  #     "playerName": "Paurush",
  #     "teamName": "Dhakkadsssss",
  #     "contestName": "mega",
  #     "secret": "xd"
  #   },
  #   {
  #     "playerName": "Paurush",
  #     "teamName": "Dhakkadsssss",
  #     "contestName": "iiitd",
  #     "secret": "xd"
  #   }
  # ]
  payload = {}
  payload['teams'] = teams
  print(payload)
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

  print(response.text)

if __name__ == "__main__":
  data = pd.read_excel("data_files/WTCFinal_IIITD.xlsx")
  contestName = 'IIITD4'
  dataFrame = pd.DataFrame(data, columns= ['Team Name', 'Full Name', 'Gold Players', 'Silver Players', 'Bronze Players', 'Captain', 'Vice Captain', 'Password'])

  teamNameToFullTeamDict = {}
  teamsWithSecretList = []
  #Removing empty lines from files
  dataFrame.dropna(subset = ["Team Name"], inplace=True)
  for index, row in dataFrame.iterrows():
    teamDataWithSecret = {}
    print(row)
    if(str(row['Team Name']).strip().lower() not in teamNameToFullTeamDict):
      teamName = str(row['Team Name']).strip().lower()
      playerName = row['Full Name']
      secret = str(row['Password']).strip()
      print(playerName)
      goldPlayers = getPlayersWithLastNamesAndLowerCase(row['Gold Players'])
      silverPlayers = getPlayersWithLastNamesAndLowerCase(row['Silver Players'])
      bronzePlayers = getPlayersWithLastNamesAndLowerCase(row['Bronze Players'])
      captain = row['Captain'].strip().lower()
      viceCaptain = row['Vice Captain'].strip().lower()
      teamNameToFullTeamDict[teamName] = teams(teamName, playerName, goldPlayers + silverPlayers + bronzePlayers, captain, viceCaptain)
      teamDataWithSecret['teamName'] = teamName
      teamDataWithSecret['playerName'] = playerName
      teamDataWithSecret['secret'] = secret
      teamDataWithSecret['contestName'] = contestName
    else:
      teamName = str(row['Team Name']).strip().lower()
      playerName2 = row['Full Name']
      secret2 = str(row['Password']).strip()
      goldPlayers2 = getPlayersWithLastNamesAndLowerCase(row['Gold Players'])
      silverPlayers2 = getPlayersWithLastNamesAndLowerCase(row['Silver Players'])
      bronzePlayers2 = getPlayersWithLastNamesAndLowerCase(row['Bronze Players'])
      captain2 = row['Captain'].strip().lower()
      viceCaptain2 = row['Vice Captain'].strip().lower()
      teamNameToFullTeamDict[teamName].setPlayer2(playerName2, goldPlayers2 + silverPlayers2 + bronzePlayers2, captain2, viceCaptain2)
      teamDataWithSecret['teamName'] = teamName
      teamDataWithSecret['playerName'] = playerName2
      teamDataWithSecret['secret'] = secret2
      teamDataWithSecret['contestName'] = contestName
    teamsWithSecretList.append(teamDataWithSecret)


  # print(teamNameToFullTeamDict.keys())
  with open("./data_files/teams/teams1.json", "w") as file1:
    file1.write("teams_iiitd = '")
    writeTeams(teamNameToFullTeamDict, file1)
    file1.write("'")
  print(teamsWithSecretList)
  print(len(teamNameToFullTeamDict.keys()))
  print(teamNameToFullTeamDict.keys())
  set_teams_in_db(teamsWithSecretList)
  

  # teamObj = teams(row['Full Name'], )

  # trim_strings = lambda x: x.strip() if isinstance(x, str) else x
  # teamNames = teamNames.applymap(trim_strings)

  # shorten_strings = lambda x: x.lower() if isinstance(x, str) else x
  # teamNames = teamNames.applymap(short_strings)

  # teamNames = teamNames.drop_duplicates()

  # 
  # for index, row in teamNames.iterrows():
  #   teamNames
  #   print(row)
  #   print(teamsList[index].x)
    


  # out = '['
  # number = input("Enter the number of teams : ")
  # for n in range(0,int(number)):
  #   out+='{'
  #   teamName = input("Enter the team Name number " + str(n+1) + ":")
  #   player1 = input("Enter the player 1 name : ")
  #   player2 = input("Enter the player 2 name : ")
  #   player1Team=[]
  #   player2Team=[]
  #   for i in range(0,7):
  #     player1Team.append(input("Enter the player1 team player number " + str(i+1) + " :"))
  #   player1Captain = input("Enter the player1 captain name : ")
  #   player1ViceCaptain = input("Enter the player1 vice captain name : ")
  #   for i in range(0,7):
  #     player2Team.append(input("Enter the player2 team player number " + str(i+1) + " :"))
  #   player2Captain = input("Enter the player2 captain name : ")
  #   player2ViceCaptain = input("Enter the player2 vice captain name : ")
    



  #   out+="\"teamName\": \"" + teamName + "\",\"player1\":\"" + player1 +"\",\"player2\":\"" + player2+"\","
  #   out+="\"team1\": ["
    
  #   for i in range(0,7):
  #       out+="\"" + player1Team[i] + "\","
  #   out= out[:-1]
  #   out+= "],"

  #   out+="\"team2\": ["
  #   for i in range(0,7):
  #       out+="\"" + player2Team[i] + "\","
  #   out= out[:-1]
  #   out+= "],"

  #   out+= "\"team1Captain\":\"" +  player1Captain + "\","
  #   out+= "\"team1ViceCaptain\":\"" +  player1ViceCaptain + "\","
  #   out+= "\"team2Captain\":\"" +  player2Captain + "\","
  #   out+= "\"team2Captain\":\"" +  player2ViceCaptain + "\""
  #   out+='},'
  # out=out[:-1]
  # out+=']'

  
