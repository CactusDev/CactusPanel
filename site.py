from app import app, socketio

if __name__ == "__main__":
    # Using socketio.run instead of app.run because we need to support socketio
    # MAKE SURE TO REMOVE PORT AND DEBUG!
    socketio.run(app, debug=True, host="0.0.0.0", port=8000)
