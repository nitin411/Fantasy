import json
import pandas as pd

class teams:
  teamName = ""
  playerName = ""
  subIn = ""
  subOut = ""
  subDay = ""

  def __init__(self, teamName, playerName, subIn, subOut, subDay):
  	self.teamName = teamName
  	self.playerName = playerName
  	self.subIn = subIn
  	self.subOut = subOut
  	self.subDay = subDay

if __name__ == "__main__":
  data = pd.read_excel("./data_files/Subs.xlsx")
  dataFrame = pd.DataFrame(data, columns= ['Team Name','Player Name', 'Sub In', 'Sub Out', 'Sub Day'])
  subs = []
  for index, row in dataFrame.iterrows():
  	subs.append(teams(row['Team Name'], row['Player Name'], row['Sub In'], row['Sub Out'], row['Sub Day']))
  with open("./data_files/teams/subs.json", "w") as file1:
    file1.write("subs = '")
    json_string = json.dumps([ob.__dict__ for ob in subs])
    file1.write(json_string)
    file1.write("'")
