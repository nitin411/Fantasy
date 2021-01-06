import requests
import json
import subprocess

teams = '[{"teamName": "Swagglers","player1": "Rahul","player2": "Paurush","team1": ["Rahane","Warner","Rohit","Bumrah"],"team2": ["Rahane","Warner","Rohit","Bumrah"],"team1Captain": "Bumrah","team2Captain": "Bumrah","team1ViceCaptain": "Rohit","team2ViceCaptain": "Rohit"},{"teamName": "Dhaakads","player1": "Utkarsh","player2": "Abhishek","team1": ["Rahane","Warner","Rohit","Bumrah"],"team2": ["Rahane","Warner","Rohit","Bumrah"],"team1Captain": "Bumrah","team2Captain": "Bumrah","team1ViceCaptain": "Rohit","team2ViceCaptain": "Rohit"}]';


if __name__ == "__main__":
  out = '['
  number = input("Enter the number of teams : ")
  for n in range(0,int(number)):
    out+='{'
    teamName = input("Enter the team Name number " + str(n+1) + ":")
    player1 = input("Enter the player1 name : ")
    player2 = input("Enter the player2 name : ")
    player1Team=[]
    player2Team=[]
    for i in range(0,7):
      player1Team.append(input("Enter the player1 team player number " + str(i+1) + " :"))
    player1Captain = input("Enter the player1 captain name : ")
    player1ViceCaptain = input("Enter the player1 vice captain name : ")
    for i in range(0,7):
      player2Team.append(input("Enter the player2 team player number " + str(i+1) + " :"))
    player2Captain = input("Enter the player2 captain name : ")
    player2ViceCaptain = input("Enter the player2 vice captain name : ")
    



    out+="\"teamName\": \"" + teamName + "\",\"player1\":\"" + player1 +"\",\"player2\":\"" + player2+"\","
    out+="\"team1\": ["
    
    for i in range(0,7):
        out+="\"" + player1Team[i] + "\","
    out= out[:-1]
    out+= "],"

    out+="\"team2\": ["
    for i in range(0,7):
        out+="\"" + player2Team[i] + "\","
    out= out[:-1]
    out+= "],"

    out+= "\"team1Captain\":\"" +  player1Captain + "\","
    out+= "\"team1ViceCaptain\":\"" +  player1ViceCaptain + "\","
    out+= "\"team2Captain\":\"" +  player2Captain + "\","
    out+= "\"team2Captain\":\"" +  player2ViceCaptain + "\""
    out+='},'
  out=out[:-1]
  out+=']'

  with open("teams.json", "w") as file1:
    file1.write("teams = '")
    file1.write(out)
    file1.write("'")
