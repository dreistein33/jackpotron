// WebSocket Client
function colorLinesOnCircle(users) {
    let start = 0;
    let end = 0;

    for (let x = 0; x < users.length; x++) {
        var us = users[x];
        end += Math.floor(us.probability * 100);  
        console.log("Coloring: " + us.sender);
        if (end == 99) {
            end++;
        }
        const lines = $("#line-container .line");
        var userDiv = $("#user" + us.sender);

        for (let i = start; i < end; i++) {
            lines.eq(i).css({"backgroundColor": userDiv.attr("potcolor")});
        }

        start = end;
    }
}
  
function buildFrontend() {
    const socket = io("ws://localhost:4998");

    function requestData() {
        socket.emit("data");
    }

    socket.on("connect", function() {
        requestData();
    });

    socket.on("response", (data) => {
        if (data.status == "started") {
            console.log("started");
            /* 
            Aktualizuj dane:
            Id
            Users
            Lines colors
            Time end
            */
        if (!(data.winner == null)) {
            winnerDiv.text("Winner: " + data.winner);
        } 

        if (timerDiv.text().length >= 0 && timerDiv.text().length <= 20) {
            runTimer(data.end_time);      
        } 

        $("#sin").text(data.id);
        
        
        if (data.users.length > 0) {
            for (var i = 0; i < data.users.length; i++) {
            
            var us = data.users[i];
            var users = $("#user" + us.sender);

            // Check if div with given id already exists.
            if (users.length == 0) {
                // Create new div with given id.
                console.log("Adding new user");
                newDiv = $("<div id=user" + us.sender + "></div>");
                const userColor = "#" + Math.floor(Math.random()*16777215).toString(16);
                newDiv.attr("potColor", userColor);
                newDiv.text("User: " + us.sender.slice(0, 5) + " Amount: " + us.amount + " Chances: " + us.probability.toFixed(2));
                $("#users").append(newDiv);
            } 
            else {
                // Update existing div.
                console.log("updating user");
                existingDiv = $("#user" + us.sender);
                existingDiv.text("User: " + us.sender.slice(0, 5) + " Amount: " + us.amount + " Chances: " + us.probability.toFixed(2));
            }
        colorLinesOnCircle(data.users);
        } 
        } else {
        // Clear the content if new response is empty.
        }}
        else if (data.status == "ended") {
            console.log("ended");
            $("#users").empty();
            $("#winner").text(data.winner)
            // Wywolaj animacje
            // Wyswietl zwyciezce 
        }
    });
}

$(document).ready(buildFrontend);