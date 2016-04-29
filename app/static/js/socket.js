var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    socket.emit('connection', true);

    console.log("Connected to the live server!");
});

socket.on("reconnect_error", function() {
    console.log("Unable to connect to the live server. Trying again.");
});
