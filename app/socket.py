from app import socketio


@socketio.on('connection')
def handle_message(recv):
    print("Got connection with status: " + str(recv))


@socketio.on('updateAlerts')
def handle(recv):
    print(recv)
    socketio.emit('updateComplete')
