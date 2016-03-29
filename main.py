from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
engine = create_engine('sqlite:////data/user.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


# Main route
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Login route
@app.route('/login', methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        if request.form['username'] != "f" or request.form['password'] != "f":
            error = "Invalid credentials."
        else:
            return render_template('panel')
    return render_template('login', error=error)


if __name__ == '__main__':
    # init_db()
    app.run()
