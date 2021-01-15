import requests
import json
import subprocess
import pandas as pd
import numpy
import itertools


class teams:
  teamName = ""
  player1 = ""
  player2 = ""
  player3 = ""
  player4=""
  team1 = ""
  team2 = ""
  team3 = ""
  team4 = ""
  team1Captain = ""
  team1ViceCaptain = ""
  team2Captain = ""
  team2ViceCaptain = ""
  team3Captain = ""
  team3ViceCaptain = ""
  team4Captain = ""
  team4ViceCaptain = ""
   
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

  def setPlayer3(self, player3, team3, team3Captain, team3ViceCaptain):
    self.player3 = player3 
    self.team3 = team3
    self.team3Captain = team3Captain
    self.team3ViceCaptain = team3ViceCaptain

  def setPlayer4(self, player4, team4, team4Captain, team4ViceCaptain):
    self.player4 = player4 
    self.team4 = team4
    self.team4Captain = team4Captain
    self.team4ViceCaptain = team4ViceCaptain

  def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

def getPlayersWithLastNamesAndLowerCase(playersList): 
  players = playersList.split(',')
  players = numpy.char.strip(players)
  return [i.split(' ')[1].lower() for i in players]

def writeTeams(teamNameToFullTeamDict, file1):
  teamsList = []
  for team in teamNameToFullTeamDict:
    teamsList.append(teamNameToFullTeamDict[team])
  json_string = json.dumps([ob.__dict__ for ob in teamsList])
  file1.write(json_string)

if __name__ == "__main__":
  data = pd.read_excel("./data_files/MegaContestFourVFour.xlsx")
  dataFrame = pd.DataFrame(data, columns= ['Team Name', 'Full Name', 'Gold Players', 'Silver Players', 'Bronze Players', 'Captain', 'Vice Captain'])
  
  teamNameToFullTeamDict = {}
  
  #Removing empty lines from files
  dataFrame.dropna(subset = ["Team Name"], inplace=True)
  for index, row in dataFrame.iterrows():
    if(row['Team Name'].strip().lower() not in teamNameToFullTeamDict):
      teamName = row['Team Name'].strip().lower()
      playerName = row['Full Name']
      goldPlayers = getPlayersWithLastNamesAndLowerCase(row['Gold Players'])
      silverPlayers = getPlayersWithLastNamesAndLowerCase(row['Silver Players'])
      bronzePlayers = getPlayersWithLastNamesAndLowerCase(row['Bronze Players'])
      captain = row['Captain'].strip().split(' ')[1].lower()
      viceCaptain = row['Vice Captain'].strip().split(' ')[1].lower()
      teamNameToFullTeamDict[teamName] = teams(teamName, playerName, goldPlayers + silverPlayers + bronzePlayers, captain, viceCaptain)
    else:
      teamName = row['Team Name'].strip().lower()
      playerName2 = row['Full Name']
      goldPlayers2 = getPlayersWithLastNamesAndLowerCase(row['Gold Players'])
      silverPlayers2 = getPlayersWithLastNamesAndLowerCase(row['Silver Players'])
      bronzePlayers2 = getPlayersWithLastNamesAndLowerCase(row['Bronze Players'])
      captain2 = row['Captain'].strip().split(' ')[1].lower()
      viceCaptain2 = row['Vice Captain'].strip().split(' ')[1].lower()
      if(teamNameToFullTeamDict[teamName].player2==""):
        teamNameToFullTeamDict[teamName].setPlayer2(playerName2, goldPlayers2 + silverPlayers2 + bronzePlayers2, captain2, viceCaptain2)
      elif(teamNameToFullTeamDict[teamName].player3==""):
        teamNameToFullTeamDict[teamName].setPlayer3(playerName2, goldPlayers2 + silverPlayers2 + bronzePlayers2, captain2, viceCaptain2)
      else:
        teamNameToFullTeamDict[teamName].setPlayer4(playerName2, goldPlayers2 + silverPlayers2 + bronzePlayers2, captain2, viceCaptain2)
  with open("./data_files/teams/4v4_2.json", "w") as file1:
    file1.write("teams = '")
    writeTeams(teamNameToFullTeamDict, file1)
    file1.write("'")
  

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

  
