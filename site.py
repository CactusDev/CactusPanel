from app import app, socketio, config

if __name__ == "__main__":

    # Using socketio.run instead of app.run because we need to support socketio
    # MAKE SURE TO REMOVE PORT AND DEBUG!
    print(config)
    socketio.run(app, debug=config.debug, port=config.port, host=config.host)
