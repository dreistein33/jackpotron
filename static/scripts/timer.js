function runTimer(endTime) {
    var timerDiv = $("#timer");
    var endTimeMsMoment = moment.unix(endTime);

    intervalId = setInterval(function() {
        var remainingSeconds = endTimeMsMoment.diff(moment(), "seconds");

        if (remainingSeconds < 0) {
            timerDiv.text("Lottery ends in: ");
            clearInterval(intervalId);
        } else {
            remainingTime = moment.duration(remainingSeconds, "seconds");
            timerDiv.text("Lottery ends in: " + remainingTime.minutes() + "m" + remainingTime.seconds() + "s");
        }
    }, 1000);
}