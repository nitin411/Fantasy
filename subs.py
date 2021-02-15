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
  dataFrame = pd.DataFrame(data)
  subs = []
  firstRow = ""
  for index, row in dataFrame.iterrows():
    playerName = ""
    teamName=""
    subIn=""
    subOut=""
    subDay=3
    if index==1000:
      # break
      print(index)
    else:
      print("index", index)
      for (columnName, columnData) in row.iteritems():
        print("Name", columnName)
        print("Data", columnData)
        if columnName=="Your Name":
          playerName = columnData.lower()
        if columnName=="Team Name":
          teamName = columnData.lower()
        if columnData == "Sub in":
          subIn = columnName.split('[')[1][:-1]
        if columnData == "Sub out":
          subOut = columnName.split('[')[1][:-1]
      subs.append(teams(teamName, playerName, subIn, subOut, subDay))
  with open("./data_files/teams_subs/subs_iiitd3.json", "w") as file1:
    file1.write("subs = '")
    json_string = json.dumps([ob.__dict__ for ob in subs])
    file1.write(json_string)
    file1.write("'")
