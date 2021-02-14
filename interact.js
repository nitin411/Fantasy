var pointsTable = JSON.parse(data);
var myTeams = JSON.parse(teams);
var scoreboard = JSON.parse(scoreboard);
var subs = JSON.parse(subs);

var day1Snapshot = JSON.parse(data_day_1);
var day2Snapshot = JSON.parse(data_day_2);
var day3Snapshot = JSON.parse(data_day_3);
var day4Snapshot = JSON.parse(data_day_4);

var scores = [];
var teams = [];

for(var i=0; i<myTeams.length; i++) {

  var teamName = myTeams[i].teamName;
  var subsForTeam = [];
  var players = 0;

  if (myTeams[i].team1 != null && myTeams[i].team2 != null) {
    
    myTeams[i].subs = [{}, {}]

    players+=1
    myTeams[i].team1 = myTeams[i].team1.map(function(v) {
      return v.toLowerCase();
    })

    players+=1;
    myTeams[i].team2 = myTeams[i].team2.map(function(v) {
      return v.toLowerCase();
    })

    if (myTeams[i].team3) {
      players += 1; 
      myTeams[i].subs.push({})
      myTeams[i].team3 = myTeams[i].team3.map(function(v) {
        return v.toLowerCase();
      })
    } else {
      myTeams[i].team3Captain = "";
      myTeams[i].team3ViceCaptain = "";
    }

    if (myTeams[i].team4) {
      players += 1;
      myTeams[i].subs.push({})
      myTeams[i].team4 = myTeams[i].team4.map(function(v) {
        return v.toLowerCase();
      })
    } else {
      myTeams[i].team4Captain = "";
      myTeams[i].team4ViceCaptain = "";
    }

  

    myTeams[i].players = [myTeams[i].player1, myTeams[i].player2, myTeams[i].player3, myTeams[i].player4]
    myTeams[i].teams = [myTeams[i].team1, myTeams[i].team2, myTeams[i].team3, myTeams[i].team4]
    myTeams[i].teamCaptains = [myTeams[i].team1Captain.toLowerCase(), myTeams[i].team2Captain.toLowerCase(), myTeams[i].team3Captain.toLowerCase(), myTeams[i].team4Captain.toLowerCase()]
    myTeams[i].teamViceCaptains = [myTeams[i].team1ViceCaptain.toLowerCase(), myTeams[i].team2ViceCaptain.toLowerCase(), myTeams[i].team3ViceCaptain.toLowerCase(), myTeams[i].team4ViceCaptain.toLowerCase()]
    myTeams[i].badSubIn = [null, null, null, null];
    myTeams[i].badSubOut = [null, null, null, null];

    for (var j=0; j< subs.length; j++) {
      if (subs[j].teamName.toLowerCase() === teamName.toLowerCase()) {
        for (var k=0; k<players; k++){
          if (myTeams[i].players[k].toLowerCase().includes(subs[j].playerName.toLowerCase())) {
            subs[j]["subIn"] = subs[j]["subIn"].toLowerCase()
            subs[j]["subOut"] = subs[j]["subOut"].toLowerCase()
            if (!myTeams[i].teams[k].includes(subs[j]["subIn"]) && myTeams[i].teams[k].includes(subs[j]["subOut"])) {
              myTeams[i].subs[k] = subs[j]
              myTeams[i].subs[k]["subIn"] = myTeams[i].subs[k]["subIn"].toLowerCase()
              myTeams[i].subs[k]["subOut"] = myTeams[i].subs[k]["subOut"].toLowerCase()
              subs[j]["marked"] = true;
            } else {
              myTeams[i].badSubIn[k] = subs[j]["subIn"].toLowerCase()
              myTeams[i].badSubOut[k] = subs[j]["subOut"].toLowerCase()
            }
          }
        }
      }
    }

    teams.push(myTeams[i])
    myTeams[i].scores = scorePerTeam(myTeams[i]);
  }

}

var badSubs = [];
for(var i=0; i< subs.length; i++) {
  if (!subs[i]["marked"]) {
    badSubs.push(subs[i])
  }
}
console.log(badSubs)
// console.log(myTeams)

myTeams = teams
myTeams.sort(function(a, b) {
  return b.scores.totalScore - a.scores.totalScore;
});

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }

  if (!event.target.matches('.dropbtn2')) {
    var dropdowns = document.getElementsByClassName("dropdown-content2");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

function getSnapshotFromDay(day) {
  if (day === 1) {
    return day1Snapshot
  } else if (day === 2) {
    return day2Snapshot
  } else if (day === 3) {
    return day3Snapshot
  } else if (day === 4) {
    return day4Snapshot
  }
}

function handleSubstitution(team, subDay, subIn, subOut, captain, viceCaptain, score, pointsTable) {
  var multiplier = 1;
  var snapshot = getSnapshotFromDay(subDay)
  if (team.includes(subOut)) {

    if (subOut === captain) {
      multiplier = 2;
    } else if (subOut === viceCaptain) {
      multiplier = 1.5;
    }

    var oldPlayerTotalScore = pointsTable[subOut]*multiplier;
    var oldPlayerScoreToAdd = snapshot[subOut]*multiplier;
    // Removing the multiplier because sub in should only have 1x points, even if he is C/VC
    var newPlayerScoreToAdd = (pointsTable[subIn] - snapshot[subIn]);
    score = score + newPlayerScoreToAdd + oldPlayerScoreToAdd - oldPlayerTotalScore;
    
    return {score, oldPlayerScoreToAdd, newPlayerScoreToAdd};
  }
  return { score, oldPlayerScoreToAdd, newPlayerScoreToAdd };
}

function scorePerTeam(team) {
  var players = [team.team1, team.team2, team.team3, team.team4]
  var scores = [0, 0, 0, 0]
  var bonuses = [0, 0, 0, 0]
  var subInScores = [0, 0, 0, 0]
  var subOutScores = [0, 0, 0, 0]
  var teamCaptains = [team.team1Captain, team.team2Captain, team.team3Captain, team.team4Captain]
  var teamViceCaptains = [team.team1ViceCaptain, team.team2ViceCaptain, team.team3ViceCaptain, team.team4ViceCaptain]

  team["playerPoints"] = []
  for (var j=0; j<players.length; j++){
    if (players[j]) {
      team["playerPoints"].push({})
      var subbed = false;
      for(var i=0; i < players[j].length; i++ ) {

        var multiplier = 1;
        var isSubOut = team.subs[j] && (team.subs[j]["subOut"] === players[j][i])
        var isCaptain = teamCaptains[j] === players[j][i]
        var isViceCaptain = teamViceCaptains[j] == players[j][i]

        if (isCaptain) multiplier = 2;
        if (isViceCaptain) multiplier = 1.5;

        if (isSubOut) {
          subbed = true;
          var snapshot = getSnapshotFromDay(team.subs[j]["subDay"]);
          team["playerPoints"][j][players[j][i].toLowerCase()] = [snapshot[players[j][i].toLowerCase()]["score"]*multiplier + snapshot[players[j][i].toLowerCase()]["bonus"]*multiplier]
          scores[j] += snapshot[players[j][i].toLowerCase()]["score"]*multiplier
          bonuses[j] += snapshot[players[j][i].toLowerCase()]["bonus"]*multiplier
        } else {
          console.log(" player " + players[j][i].toLowerCase());
          team["playerPoints"][j][players[j][i].toLowerCase()] = [pointsTable[players[j][i].toLowerCase()]["score"]*multiplier + pointsTable[players[j][i].toLowerCase()]["bonus"]*multiplier]
          scores[j] += pointsTable[players[j][i].toLowerCase()]["score"]*multiplier
          bonuses[j] += pointsTable[players[j][i].toLowerCase()]["bonus"]*multiplier
        }
      }


      if (subbed) {
        var playerName = team.subs[j]["subIn"].toLowerCase();
        if (players[j].includes(playerName)) {
          console.log(team)
        }
        var snapshot = getSnapshotFromDay(team.subs[j]["subDay"]);
        team["playerPoints"][j][playerName] = [pointsTable[playerName]["score"] - snapshot[playerName]["score"]]
        scores[j] += pointsTable[playerName]["score"] - snapshot[playerName]["score"]
      } 

    }
  }
  
  // console.log(team);
  var totalScore = scores.reduce((a, b) => a + b, 0)
  totalScore += bonuses.reduce((a, b) => a + b, 0)
  return {scores, bonuses, totalScore, subOutScores, subInScores};

}

// Close the dropdown if the user clicks outside of it
