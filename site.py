from app import app, socketio


@socketio.on('connection')
def handle_message(recv):
    print("Got connection with status: " + str(recv))


if __name__ == "__main__":
    # Using socketio.run instead of app.run because we need to support socketio
    # MAKE SURE TO REMOVE PORT AND DEBUG!
    socketio.run(app, debug=True, port=8000)
