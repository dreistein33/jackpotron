// WebSocket Client

const socket = io("ws://localhost:4998");

function requestData() {
    socket.emit("data");
}

socket.on("connect", function() {
    var intervalId = setInterval(requestData, 5000);
});

socket.on("response", (response) => {
    console.log(response);
});
