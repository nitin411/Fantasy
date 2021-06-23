mega_teams = JSON.parse(teams);
iiitd_teams = JSON.parse(teams_iiitd);
player_tiers = JSON.parse(player_tiers);

var currentTeam = []


document.getElementById("authenticate-user").onclick = function() {
    var contestName = document.getElementById("inputGroupSelect01").value;
    var teamName = document.getElementById("teamName").value;
    var playerName = document.getElementById("playerName").value;
    var secretKey = document.getElementById("secretKey").value;

    if (contestName === "IIITD") {
        contestName = "IIITD4"
        teams = iiitd_teams
    } else {
        teams = mega_teams
    }
    
    for (team in teams) {
        if (teams[team].teamName.toLowerCase() === teamName.toLowerCase()) {
            var currentTeam = teams[team];
            if (currentTeam.player1.toLowerCase() === playerName.toLowerCase()) {
                var captain = currentTeam.team1Captain
                var viceCaptain = currentTeam.team1ViceCaptain
                currentTeam = currentTeam.team1
            } else if (currentTeam.player2.toLowerCase() === playerName.toLowerCase()) {
                var captain = currentTeam.team2Captain
                var viceCaptain = currentTeam.team2ViceCaptain
                currentTeam = currentTeam.team2
            } else {
                currentTeam = [];
            }
        }
    }

    var team_selector = document.getElementById("team_selector");
    while (team_selector.firstChild) {
        team_selector.removeChild(team_selector.lastChild);
      }
    
    var formCheck = document.createElement("form");
    formCheck.classList = ["form-check form-check-container"]
    formCheck.id = "formcheck"
    
    var h5 = document.createElement("h5")
    h5.appendChild(document.createTextNode("Please select a player from your team to sub out"));
    formCheck.appendChild(h5);
    formCheck.appendChild(document.createElement("br"))

    for (playerIndex in currentTeam) {

        var formCheck2 = document.createElement("div");
        formCheck2.classList = ["form-check"]
        formCheck2.id = "formcheck"

        var input = document.createElement("input");
        input.classList = "form-check-input"
        input.type = "radio"
        input.value = currentTeam[playerIndex]
        input.name = "exampleRadios"
        formCheck2.appendChild(input);

        var label = document.createElement("label");
        label.classList = "form-check-label"
        var appendedText = "";
        if (currentTeam[playerIndex] === captain ) {
            appendedText = " (C)"
        } else if (currentTeam[playerIndex] === viceCaptain) {
            appendedText = " (VC)"
        }
        label.appendChild(document.createTextNode(currentTeam[playerIndex] + appendedText));
        formCheck2.appendChild(label);

        formCheck.appendChild(formCheck2)
        
    }

    team_selector.appendChild(formCheck);

    buttonSubOut = document.createElement("button");
    formCheck.appendChild(document.createElement("br"))
    buttonSubOut.appendChild(document.createTextNode("Show Replacements"));
    buttonSubOut.id = "subOutButton"
    buttonSubOut.classList = ["btn btn-primary btn-center"]
    buttonSubOut.onclick = function(a){
        subOut = document.getElementById("formcheck").elements["exampleRadios"].value;
        tier = player_tiers[subOut];
        playersToConsider = []
        for (player in player_tiers) {
            if (player_tiers[player] === tier) {
                playersToConsider.push(player);
            }
        }
        

        var team_selector_sub_in = document.getElementById("team_selector_sub_in");
        while (team_selector_sub_in.firstChild) {
            team_selector_sub_in.removeChild(team_selector_sub_in.lastChild);
          }
        var formCheckSubIn = document.createElement("form");
        formCheckSubIn.classList = ["form-check form-check-container"]
        formCheckSubIn.id = "formcheckSubIn"

        var h5 = document.createElement("h5")
        h5.appendChild(document.createTextNode("Please select a "+ tier + " player to sub in for " + subOut ));
        formCheckSubIn.appendChild(h5);
        formCheckSubIn.appendChild(document.createElement("br"))

        for (player3 in playersToConsider) {

            var formCheckSubIn2 = document.createElement("div");
            formCheckSubIn2.classList = ["form-check"]
            formCheckSubIn2.id = "formcheckSubIn"
    
            var input = document.createElement("input");
            input.classList = "form-check-input"
            input.type = "radio"
            input.value = playersToConsider[player3]
            input.name = "exampleRadiosSubIn"

            if (currentTeam.indexOf(playersToConsider[player3]) > -1) {
                input.disabled = true;
            }
            formCheckSubIn2.appendChild(input);

    
            var label = document.createElement("label");
            label.classList = "form-check-label"
            label.appendChild(document.createTextNode(playersToConsider[player3]));
            formCheckSubIn2.appendChild(label);
    
            formCheckSubIn.appendChild(formCheckSubIn2)
            
        }

        team_selector_sub_in.appendChild(formCheckSubIn)

        button_subIn = document.createElement("button");
        formCheckSubIn.appendChild(document.createElement("br"))
        button_subIn.appendChild(document.createTextNode("Confirm Swap"));
        button_subIn.id = "subInButton"
        button_subIn.classList = ["btn btn-primary btn-center"]
        button_subIn.onclick = function(a){

            subIn = document.getElementById("formcheckSubIn").elements["exampleRadiosSubIn"].value;

            var data = new FormData();
            data.append('playerName', playerName);
            data.append('teamName', teamName);
            data.append('subIn', subIn);
            data.append('subOut', subOut);
            data.append('subDay', '5');
            data.append("contestName", contestName);
            data.append("secret", secretKey);


            var xhr = new XMLHttpRequest();
            xhr.open('POST', 'https://clash11.herokuapp.com/setsub', true);
            xhr.onload = function () {
                // do something to response
                window.alert(this.responseText);
            };
            xhr.send(data);

        }
        team_selector_sub_in.appendChild(button_subIn);
    };
    team_selector.appendChild(buttonSubOut);
};

// Set the date we're counting down to
var countDownDate = new Date("March 6, 2021 09:30:00").getTime();

// Update the count down every 1 second
var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();

  // Find the distance between now and the count down date
  var distance = countDownDate - now;

  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Display the result in the element with id="demo"
  document.getElementById("countdown").innerHTML = "No more substitutions allowed in the game";

  // If the count down is finished, write some text
  if (distance < 0) {
    clearInterval(x);
    document.getElementById("demo").innerHTML = "EXPIRED";
  }
}, 1000);