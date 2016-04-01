var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    socket.emit('connection', true);

    // diag
    console.log("Connection to socket.io worked.");
});
