var pointsTable = JSON.parse(data);
var myTeams = JSON.parse(teams);
var scoreboard = JSON.parse(scoreboard);

var day1Snapshot = JSON.parse(day1Snap);
var day2Snapshot = JSON.parse(data_day_2);
var day3Snapshot = JSON.parse(data_day_3);
var day4Snapshot = JSON.parse(data_day_4);

var scores = [];
var teams = [];

console.log(myTeams.length)
for(var i=0; i<myTeams.length; i++) {

  if (myTeams[i].team1 != null && myTeams[i].team2 != null) {
    myTeams[i].team1 = myTeams[i].team1.map(function(v) {
      return v.toLowerCase();
    })
    myTeams[i].team2 = myTeams[i].team2.map(function(v) {
      return v.toLowerCase();
    })

    if (myTeams[i].team3) {
      myTeams[i].team3 = myTeams[i].team3.map(function(v) {
        return v.toLowerCase();
      })
    } else {
      myTeams[i].team3Captain = "";
      myTeams[i].team3ViceCaptain = "";
    }

    if (myTeams[i].team4) {
      myTeams[i].team4 = myTeams[i].team4.map(function(v) {
        return v.toLowerCase();
      })
    } else {
      myTeams[i].team4Captain = "";
      myTeams[i].team4ViceCaptain = "";
    }

    console.log(myTeams[i])
    myTeams[i].scores = scorePerTeam(myTeams[i]);
    myTeams[i].players = [myTeams[i].player1, myTeams[i].player2, myTeams[i].player3, myTeams[i].player4]
    myTeams[i].teams = [myTeams[i].team1, myTeams[i].team2, myTeams[i].team3, myTeams[i].team4]
    myTeams[i].teamCaptains = [myTeams[i].team1Captain.toLowerCase(), myTeams[i].team2Captain.toLowerCase(), myTeams[i].team3Captain.toLowerCase(), myTeams[i].team4Captain.toLowerCase()]
    myTeams[i].teamViceCaptains = [myTeams[i].team1ViceCaptain.toLowerCase(), myTeams[i].team2ViceCaptain.toLowerCase(), myTeams[i].team3ViceCaptain.toLowerCase(), myTeams[i].team4ViceCaptain.toLowerCase()]
  
    teams.push(myTeams[i])
  }

}

myTeams = teams
myTeams.sort(function(a, b) {
  return b.scores.totalScore - a.scores.totalScore;
});
console.log(myTeams.length)

console.log(myTeams)

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
  if (day === "1") {
    return day1Snapshot
  } else if (day === "2") {
    return day2Snapshot
  } else if (day === "3") {
    return day3Snapshot
  } else if (day === "4") {
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
  var substitute = team.substitutes;

  for (var j=0; j<players.length; j++){
    if (players[j]) {
      for(var i=0; i < players[j].length; i++ ) {
        scores[j] += pointsTable[players[j][i].toLowerCase()]["score"]
        bonuses[j] += pointsTable[players[j][i].toLowerCase()]["bonus"]
      }

      scores[j] += pointsTable[teamCaptains[j].toLowerCase()]["score"]
      bonuses[j] += pointsTable[teamCaptains[j].toLowerCase()]["bonus"]
      scores[j] += 0.5*pointsTable[teamViceCaptains[j].toLowerCase()]["score"]
      bonuses[j] += 0.5*pointsTable[teamViceCaptains[j].toLowerCase()]["bonus"]

      // if (substitute && substitute.sub1Day !== "") {
      //   var subLogic = handleSubstitution(players[j], substitute.player[j]["day"], substitute.player[j]["in"], substitute.player[j]["out"], 
      //   teamCaptains[j], teamViceCaptains[j], scores[j], pointsTable);

      //   scores[j] = subLogic.score
      //   subOutScores[j] = subLogic.oldPlayerScoreToAdd
      //   subInScores[j] = subLogic.newPlayerScoreToAdd
      // }
    }
  }
  
  var totalScore = scores.reduce((a, b) => a + b, 0)
  return {scores, totalScore, subOutScores, subInScores};

}

// Close the dropdown if the user clicks outside of it
