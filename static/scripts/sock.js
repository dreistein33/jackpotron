// WebSocket Client

//Pokolorowanie lini na bialo
function colorAllLines() {
    const lines = $("#spin .line");
    lines.css({"backgroundColor": "#f5f5f5"});
}
//Pokolorowanie lini wedle szans uzytkownikow
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
        const lines = $("#spin .line");
        var userDiv = $("#user" + us.sender);

        for (let i = start; i < end; i++) {
            lines.eq(i).css({"backgroundColor": userDiv.attr("potcolor")});
        }

        start = end;
    }
}

function runTimer(endTime) {
    var timerDiv = $("#timer");
    var endTimeMsMoment = moment.unix(endTime);

    intervalId = setInterval(function() {
        var remainingSeconds = endTimeMsMoment.diff(moment(), "seconds");

        if (remainingSeconds < 0) {
            timerDiv.text("! DRAWING WINNER !");
            clearInterval(intervalId);
        } else {
            remainingTime = moment.duration(remainingSeconds, "seconds");
            timerDiv.text("TO END " + remainingTime.minutes() + " M " + remainingTime.seconds() + " s");
        }
    }, 1000);
}
  
function buildFrontend() {
    const socket = io("ws://localhost:4998");

    function requestData() {
        socket.emit("data");
        socket.emit("history");
    }

    socket.on("connect", function() {
        requestData();
    });

    // HISTORY DATA
    socket.on("last", (data) => {

        
        tableDiv = $("<div id=table></div>");
        for (let i = data.length - 1; i >= 0; i--) {
            if (!(data[i].winner == null)) {
                var potidDiv = $("<div class='potid'></div>");
                var winDiv = $("<div class='win'></div>");
                var ref = $("<a href=https://shasta.tronscan.org/#/address/" + data[i].winner + ">" + data[i].winner +"</a>");
                winDiv.append(ref);
                var potDiv = $("<div class='pot'></div>");

                potidDiv.text("#" + data[i].id);
                potDiv.text("$ " + data[i].prize);

                
                tableDiv.append(potidDiv);
                tableDiv.append(winDiv);
                tableDiv.append(potDiv);
        }
    }
        $("#tablebox").append(tableDiv);
        console.log(data);
    })

    // LIVE DATA
    socket.on("response", (data) => {
        console.log(data)
        if (data.status == "started") {
            console.log("started");
            /* 
            Aktualizuj dane:
            Id
            Users
            Lines colors
            Time end
            */
        var winnerDiv = $("#winner");
        if (winnerDiv.text().length > 0) {
            winnerDiv.text("");
        }
        
        if (timerDiv.text().length <= 20) {
            runTimer(data.end_time);      
        } 

        $("#id").text(data.id);
        
        
        if (data.users.length > 0) {
            for (var i = 0; i < data.users.length; i++) {
            
            var us = data.users[i];
            var users = $("#user" + us.sender);

            // Check if div with given id already exists.
        if (users.length == 0) {
            // Create new div with given id.
            console.log("Adding new user");
            newDiv = $("<div id=user" + us.sender + "></div>");

            function generateColor() {
            let r, g, b;
            const index = Math.floor(Math.random() * 3); 

            if (index === 0) {
                r = 0; 
                g = 51 * (Math.floor(Math.random() * 5) + 1);
                b = 51 * (Math.floor(Math.random() * 5) + 1);
            } else if (index === 1) {
                r = 51 * (Math.floor(Math.random() * 5) + 1);
                g = 0;
                b = 51 * (Math.floor(Math.random() * 5) + 1);
            } else {
                r = 51 * (Math.floor(Math.random() * 5) + 1);
                g = 51 * (Math.floor(Math.random() * 5) + 1);
                b = 0;
            }

            return `rgb(${r}, ${g}, ${b})`;
            }


            const userColor = generateColor();


            newDiv.attr("potColor", userColor);

            // Create three divs inside the user div.
            var tagDiv = $("<div class='tag'></div>");
            var amountDiv = $("<div class='amount'></div>");
            var luckDiv = $("<div class='luck'></div>");

            // Set the text for each div.
            tagDiv.text("#" + us.sender.slice(0, 5));
            amountDiv.text("$ " + us.amount);
            luckDiv.text("|%| " + (us.probability.toFixed(2) * 100));

            // Add the three divs to the new user div.
            newDiv.append(tagDiv);
            newDiv.append(amountDiv);
            newDiv.append(luckDiv);

            // Set the color for the "tag" class based on the "potColor" attribute
            var potColor = newDiv.attr("potColor");
            tagDiv.css("color", potColor);
            
            $("#user").append(newDiv);
            
            



            } 
            else {
                // Update existing div.
                console.log("updating user");
                var existingDiv = $("body").find("#user" + us.sender);
                var tagDiv = existingDiv.find(".tag");
                var amountDiv = existingDiv.find(".amount");
                var luckDiv = existingDiv.find(".luck");

                // Set the text for each div.
                tagDiv.text("#" + us.sender.slice(0, 5));
                amountDiv.text("$ " + us.amount);
                luckDiv.text("|%| " + (us.probability.toFixed(2) * 100));
                
                
                existingDiv.appendTo("#user");
            }

            
            function sumAmounts() {
                var total = 0;
                $(".amount").each(function() {
                    var amount = $(this).text().replace("$", ""); 
                    total += parseFloat(amount); 
                });
                return total;
                }
                $("#prize").text("$ " + sumAmounts());

        colorLinesOnCircle(data.users);
        } 
        } else {
        // Clear the content if new response is empty.
        }}
        else if (data.status == "ended") {
            //Lottery end functions
            console.log("ended");
            colorAllLines();
            $("#timer").text("NEXT COMING")
            $("#prize").text("$ 0");
            $("#user").text("USERS");
            $("#winner").text(data.winner)


            setTimeout(function() {
                var winner = $("#winner").text();
                if (winner !== "") { // Sprawdzenie, czy winner nie jest pusty
                // Animacja przyciemnienia tła
                $("#overlay").fadeIn(500, function() {
                // Animacja wyświetlenia komunikatu z wygranym
                $("#winner").fadeIn(500).delay(5000).fadeOut(1000, function() {
                    // Animacja przywrócenia normalnego wyglądu strony
                    $("#overlay").fadeOut(1000);
                    location.reload(); //Odswiezenie strony, mozliwe ze trzeba dodac opoznienie 
                        });
                    });
                
                }
            }, 500);
            
        }
    });
}





$(document).ready(buildFrontend);