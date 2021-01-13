import json

if __name__ == "__main__":
  data = pd.read_excel("./data_files/Subs.xlsx")
  dataFrame = pd.DataFrame(data, columns= ['Player Name', 'Sub In', 'Sub Out'])
  
