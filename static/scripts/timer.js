function runTimer(endTime) {
    var timerDiv = $(".timer #timer");
    var endTimeMsMoment = moment.unix(endTime);

    intervalId = setInterval(function() {
        var remainingSeconds = endTimeMsMoment.diff(moment(), "seconds");

        if (remainingSeconds < 0) {
            timerDiv.text("TO END ");
            clearInterval(intervalId);
        } else {
            remainingTime = moment.duration(remainingSeconds, "seconds");
            timerDiv.text("TO END " + remainingTime.minutes() + " M " + remainingTime.seconds() + " s");
        }
    }, 1000);
}