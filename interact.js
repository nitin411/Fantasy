var pointsTable = JSON.parse(data);
var myTeams = JSON.parse(teams);
var scoreboard = JSON.parse(scoreboard);

var day1Snapshot = JSON.parse(day1Snap);
var day2Snapshot = JSON.parse(data_day_2);
var day3Snapshot = JSON.parse(data_day_3);
var day4Snapshot = JSON.parse(data_day_4);

var scores = [];

for(var i=0; i<myTeams.length; i++) {
  myTeams[i].scores = scorePerTeam(myTeams[i]);
}

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
  console.log(team);
  if (team.includes(subOut)) {
    if (subOut === captain) {
      multiplier = 2;
    } else if (subOut === viceCaptain) {
      multiplier = 1.5;
    }

    var scoreToRemove = snapshot[subOut]*multiplier;
    var scoreToAdd = (pointsTable[subIn] - snapshot[subIn])*multiplier;
    return score + scoreToAdd - scoreToRemove;
  }
  return score;
}

function scorePerTeam(team) {
  var players1 = team.team1;
  var players2 = team.team2;
  var players3 = team.team3;
  var players4 = team.team4;
  var score1 = 0;
  var score2 = 0;
  var score3 = 0;
  var score4 = 0;
  var substitute = team.substitutes;

  for(var i=0; i < players1.length; i++ ) {
    score1 += pointsTable[players1[i]]
  }
  score1 += pointsTable[team.team1Captain]
  score1 += 0.5*pointsTable[team.team1ViceCaptain]
  if (substitute && substitute.sub1Day !== "") {
    score1 = handleSubstitution(players1, substitute.sub1Day, substitute.sub1In, substitute.sub1Out, 
      team.team1Captain, team.team1ViceCaptain, score1, pointsTable);
  }

  for(var i=0; i < players2.length; i++ ) {
    score2 += pointsTable[players2[i]]
  }
  score2 += pointsTable[team.team2Captain]
  score2 += 0.5*pointsTable[team.team2ViceCaptain]
  if (substitute && substitute.sub2Day !== "") {
    score2 = handleSubstitution(players2, substitute.sub2Day, substitute.sub2In, substitute.sub2Out, 
      team.team2Captain, team.team2ViceCaptain, score2, pointsTable);
  }

  if (players3){
    for(var i=0; i < players3.length; i++ ) {
      score3 += pointsTable[players3[i]]
    }
    score3 += pointsTable[team.team3Captain]
    score3 += 0.5*pointsTable[team.team3ViceCaptain]
    if (substitute && substitute.sub3Day !== "") {
      score3 = handleSubstitution(players3, substitute.sub3Day, substitute.sub3In, substitute.sub3Out, 
        team.team3Captain, team.team3ViceCaptain, score3, pointsTable);
    }
  }

  if (players4){
    for(var i=0; i < players4.length; i++ ) {
      score4 += pointsTable[players4[i]]
    }
    score4 += pointsTable[team.team4Captain]
    score4 += 0.5*pointsTable[team.team4ViceCaptain]
    if (substitute && substitute.sub4Day !== "") {
      score4 = handleSubstitution(players4, substitute.sub4Day, substitute.sub4In, substitute.sub4Out, 
        team.team4Captain, team.team4ViceCaptain, score4, pointsTable);
    }
  }

  

  var totalScore = score1+score2+score3+score4;

  return {score1, score2, score3, score4, totalScore};

}

// Close the dropdown if the user clicks outside of it
