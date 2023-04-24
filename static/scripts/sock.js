// WebSocket Client

// Funkcja do przejścia na pełny ekran
function toggleFullscreen() {
    var doc = window.document;
    var docEl = doc.documentElement;
    var requestFullscreen = docEl.requestFullscreen || docEl.mozRequestFullScreen || docEl.webkitRequestFullScreen || docEl.msRequestFullscreen;
    var exitFullscreen = doc.exitFullscreen || doc.mozCancelFullScreen || doc.webkitExitFullscreen || doc.msExitFullscreen;
    if (!doc.fullscreenElement && !doc.mozFullScreenElement && !doc.webkitFullscreenElement && !doc.msFullscreenElement) {
        
        requestFullscreen.call(docEl);
    } else {
        
        exitFullscreen.call(doc);
    }
}





//Pokolorowanie lini na bialo
function colorAllLines() {
    const lines = $("#spin .line");
    lines.css({"backgroundColor": "#999999"});
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

var soundOn = new Audio('static/aud/soundon.mp3');
var audioEnabled = false;
var audioToggle = document.querySelector("#mutebutton > img");
var speakerOnImg = "static/imag/speaker.svg";
var speakerOffImg = "static/imag/speakerx.svg";

function toggleAudio() {
  audioEnabled = !audioEnabled;
  if (audioEnabled) {
    beep.volume = 1;
    beepx.volume = 1;
    last10.volume = 1;
    last30.volume = 1;
    last1.volume = 1;
    soundOn.volume = 1;
    audioToggle.src = speakerOnImg;
    soundOn.play();
    console.log("SOUND ON")
  } else {
    beep.volume = 0;
    beepx.volume = 0;
    last10.volume = 0;
    last30.volume = 0;
    last1.volume = 0;
    soundOn.volume = 0;
    audioToggle.src = speakerOffImg;
    console.log("SOUND OFF")
  }
}

audioToggle.addEventListener("click", toggleAudio);


var spin = document.querySelector("#spin");
var beep = new Audio('static/aud/hitic.mp3');
beep.volume = 0;
var beepx = new Audio('static/aud/lowtic.mp3');
beepx.volume = 0;
var last10 = new Audio('static/aud/10last.mp3');
last10.volume = 0;
var last30 = new Audio('static/aud/30s.mp3');
last30.volume = 0;
var last1 = new Audio('static/aud/last1.mp3');
last1.volume = 0;

function runTimer(endTime) {
    var timerDiv = $("#timer");
    var endTimeMsMoment = moment.unix(endTime);
    
    // Calculate initial animation duration
    var remainingSeconds = endTimeMsMoment.diff(moment(), "seconds");
    var animationDuration = remainingSeconds + "s";
    spin.style.setProperty("animation-duration", animationDuration);
    console.log(animationDuration);
    intervalId = setInterval(function() {
        remainingSeconds = endTimeMsMoment.diff(moment(), "seconds");

        if (remainingSeconds < 0) {
            timerDiv.text("! DRAWING WINNER !");
            clearInterval(intervalId);
        } else {
            remainingTime = moment.duration(remainingSeconds, "seconds");
            timerDiv.text("TO END " + remainingTime.minutes() + " M " + remainingTime.seconds() + " s");
            
            // Update animation duration based on the initial value
            spin.style.setProperty("animation-duration", animationDuration);
            

            if (remainingSeconds === 11) {
                last10.play();
            }
            if (remainingSeconds === 31) {
                last30.play();
            }
            if (remainingSeconds === 61) {
                last1.play();
            }
            if (remainingSeconds <= 10) {
                beep.play();
            }
            if (remainingSeconds % 60 === 0) {
                beepx.play();
            }


        }
    }, 1000);
}


function generateQrCode(address, amount, memo) {
    var wallet_url = `tron:${address}?token=TRX&amount=${amount}&note=${memo}`;
    var qrContainer = $("#qrcode");
    qrContainer.attr("src", `https://api.qrcode-monkey.com/qr/custom?size=128&${encodeURIComponent(wallet_url)}`);
    $("panel").append(qrContainer);
}

function copyToClipboard() {
  var divToCopy = document.querySelector("h2");
  var textToCopy = divToCopy.innerText;
  navigator.clipboard.writeText(textToCopy)
    .then(function() {
      alert("COPIED! : " + textToCopy);
    }, function() {
      alert("ERROR!");
    });
}


var isTransformed = false;

function transformButton() {
  // Pobranie elementów przycisku i boxa
  var history = document.querySelector(".history");
  var historytitle = document.getElementById("historytitle");
  var button = document.getElementById("adrbutton");
  var infobox = document.querySelector(".infobox");
  var qrcode = document.getElementById("qrcode");
  var h2style = document.querySelector("h2");
  var addressbox = document.getElementById("addressbutton");
  // Sprawdzenie aktualnego stanu przycisku
  if (isTransformed) {
      //  OFF
      addressbox.style.backgroundColor = "#1b1b1b";
      historytitle.style.width = "100%";
      historytitle.style.left = "0%";
      button.style.width = "100%";
      button.style.marginLeft = "0%";
      h2style.style.fontSize = "0vw";
      qrcode.classList.remove("hidden");
      history.style.height = "90vh";
      infobox.style.height = "0vh";
      button.textContent = "[ TAB FOR INFO ]";
      button.style.backgroundColor = "#1b1b1b";
      console.log("Close");
      
  } else {
      // ON
      addressbox.style.backgroundColor = "#2b2b2b";
      historytitle.style.width = "90%";
      historytitle.style.left = "5%";
      button.style.width = "90%";
      button.style.marginLeft = "5%";
      h2style.style.fontSize = "1.1vw";
      infobox.style.height = "45vh";
      qrcode.classList.add("hidden");
      history.style.height = "45vh";
      button.textContent = "[ TAB TO CLOSE ]";
      button.style.backgroundColor = "#2c2c2c";
      console.log("Open");

  }

  // Zmiana stanu przycisku (toggle)
  isTransformed = !isTransformed;
}

// Obsługa klawisza Tab
document.addEventListener('keydown', function(event) {
  if (event.code === 'Tab') {
    event.preventDefault(); // Zatrzymaj domyślną akcję przeglądarki dla klawisza Tab
    transformButton();
  }
});

function autoButton() {
    setTimeout(transformButton, 2500);
    setTimeout(transformButton, 10000);
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

        var lastHistoryData;

        var highestPrize = 0;
        var totalPrize = 0;

        var highestPrizeDiv = $("<div id=highest-prize></div>");
        var totalPrizeDiv = $("<div id=total-prize></div>");



        tableDiv = $("<div id=table></div>");
        if (lastHistoryData != data) {
            for (let i = data.length - 1; i >= 0; i--) {
                if (!(data[i].winner == null)) {
                    if (data[i].prize > highestPrize) {
                    highestPrize = data[i].prize;
                    highestPrizeDiv.text("TOP $ " + highestPrize);
                }
                    totalPrize += data[i].prize;
                    var potidDiv = $("<div class='potid'></div>");
                    var winDiv = $("<div class='win'></div>");
                    var ref = $("<a target=_blank href=https://shasta.tronscan.org/#/address/" + data[i].winner + ">" + ((data[i].winner).slice(0,12)) +"</a>");
                    winDiv.append(ref);
                    var potDiv = $("<div class='pot'></div>");

                    potidDiv.text(data[i].id);
                    potDiv.text("$ " + data[i].prize);
                    totalPrizeDiv.text("SUM $ " + totalPrize);
                    
                    tableDiv.append(potidDiv);
                    tableDiv.append(winDiv);
                    tableDiv.append(potDiv);
            }
        }
    }
        $("#tablebox").append(tableDiv);
        $(".panel").append(highestPrizeDiv);
        $(".panel").append(totalPrizeDiv);

    })

    // LIVE DATA
    socket.on("response", (data) => {
        if (data.status == "started") {
            console.log("started");
            var b64String = `data:image/png;base64,${data.qrcode}`;
            $("#qrcode").attr("src", b64String);
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
            luckDiv.text("% " + ((us.probability.toFixed(3) * 100).toFixed(1)));

            // Add the three divs to the new user div.
            newDiv.append(tagDiv);
            newDiv.append(amountDiv);
            newDiv.append(luckDiv);

            // Set the color for the "tag" class based on the "potColor" attribute
            var potColor = newDiv.attr("potColor");
            tagDiv.css("color", potColor);
            tagDiv.css("border-left","8px solid", potColor);
            tagDiv.css("text-shadow","-5px 0px 10px", potColor);
            
            
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
                luckDiv.text("% " + ((us.probability.toFixed(3) * 100).toFixed(1)));
                
                
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
                $("#prize").text(sumAmounts());

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
            $("#prize").text("");
            $("#user").text("BET LIST EMPTY");
            $("#winner").text(data.winner)

            setTimeout(function() {
                var winner = $("#winner").text();
                if (winner !== "") { // Sprawdzenie, czy winner nie jest pusty
                    // Animacja przyciemnienia tła
                    console.log("WINNER CHOISEN, RELOADING...");
                    $("#overlay").fadeIn(500, function() {
                        // Animacja wyświetlenia komunikatu z wygranym
                        $("#winner").fadeIn(500).delay(3000).fadeOut(1000, function() {
                            // Animacja przywrócenia normalnego wyglądu strony
                            $("#overlay").fadeOut(500);
                                                   });
                    });
                    setTimeout(function() {
                        location.reload()
                }, 5000)
                } 
                else {
                    console.log("NO WINNER, RELOADING..."); // Log w konsoli przy pustym winner
                    
                }
            }, 1000);
        }
    });
}






$(document).ready(buildFrontend);