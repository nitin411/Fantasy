var pointsTable = JSON.parse(data);
var myTeams = JSON.parse(teams);
var scoreboard = JSON.parse(scoreboard);
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

function scorePerTeam(team) {
  var players1 = team.team1;
  var players2 = team.team2;
  var score1 = 0;
  var score2 = 0;

  for(var i=0; i < players1.length; i++ ) {
    score1 += pointsTable[players1[i]]
  }

  for(var i=0; i < players2.length; i++ ) {
    score2 += pointsTable[players2[i]]
  }

  score1 += pointsTable[team.team1Captain]
  score2 += pointsTable[team.team2Captain]
  score1 += 0.5*pointsTable[team.team1ViceCaptain]
  score2 += 0.5*pointsTable[team.team2ViceCaptain]
  var totalScore = score1+score2;

  return {score1, score2, totalScore};

}

// Close the dropdown if the user clicks outside of it
