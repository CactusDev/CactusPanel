from flask import Flask, render_template
from flask.ext.login import LoginManager, login_required, UserMixin

from json import load

app = Flask(__name__)
# CHANGE THIS BEFORE YOU PRODUCTION!!!!
secret = "CHANGETHISBEFOREPRODUCTION!"

# Load the config


def load_config():
    with open('data/config.json') as f:
        data = load(f)
        secret = data['secret']


# Flask-login things

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    db = {"2Cubed": ("2Cubed", "Tech"),
          "Paradigm": ("Para", "digm")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls, id):
        return cls.db.get(id)


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')

    if token is None:
        token = request.args.get('token')

    if token is not None:
        username, password = token.split(":")
        user_entry = User.get(username)

        if user_entry is not None:
            user = User(user_entry[0], user_entry[1])

            if user.password == password:
                return user
    return None


# Main route
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Login route
@app.route('/login', methods=["GET", "POST"])
def login():
    # TODO
    pass


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    # TODO
    pass


if __name__ == '__main__':
    app.config["SECRET_KEY"] = secret
    app.run()
