var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    socket.emit('connection', true);

    // diag
    console.log("Connection to socket.io worked.");
});


function send(type, message) {
  socket.emit(type, message);

  console.log("Sent data with the type of: " + type + " and the data of " + message)
}
