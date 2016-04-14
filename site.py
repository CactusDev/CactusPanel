from app import app, socketio
from flask.ext.assets import Environment, Bundle

assets = Environment(app)


@socketio.on('connection')
def handle_message(recv):
    print("Got connection with status: " + str(recv))


@socketio.on('updateAlerts')
def handle(recv):
    print(recv)
    socketio.emit('updateComplete')


if __name__ == "__main__":

    # Does some sort of magical magic. Makes it all one file because #MAGIC™!

    js = Bundle('js/libs/angular.min.js', 'js/diag.js',
                'js/libs/jquery.min.js', 'js/socket.js',
                'js/libs/angular-animate.min.js',
                'js/libs/angular-aria.min.js',
                'js/libs/angular-material.min.js',
                'js/libs/angular-messages.min.js',
                'js/libs/socket.io.min.js', 'js/angular/index.js',
                # 'js/angular/directives.js',
                filters='jsmin',
                output='js/packed.js')

    assets.register('js_all', js)

    # Don't remove that. It makes EVERYTHING work.
    app.config['ASSETS_DEBUG'] = True
    # If you remove it, I will take your cat. And your dog. And your familiy.

    # Using socketio.run instead of app.run because we need to support socketio
    # MAKE SURE TO REMOVE PORT AND DEBUG!

    socketio.run(app, debug=True, host="0.0.0.0", port=8000)
