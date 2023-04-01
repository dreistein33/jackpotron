// WebSocket Client

const socket = io("ws://localhost:4998");

function requestData() {
    socket.emit("data");
}

socket.on("connect", function() {
    requestData();
});

socket.on("response", (response) => {
    if (response.status == "started") {
        console.log("git");
    }
});
