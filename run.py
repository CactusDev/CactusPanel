from app import app, socketio

if __name__ == "__main__":
    print(app.config)
    socketio.run(app, port=app.config["PORT"], host=app.config["HOST"])
