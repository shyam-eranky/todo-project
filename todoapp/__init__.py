# Initialization of the todoapp module happens here
# Main flask app gets created using factory and the db ORM is setup
import os
import pprint as pp
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Setup DB
db = SQLAlchemy()
login = LoginManager()


def print_config():
    pp.pprint(current_app.config['SECRET_KEY']) 
    pp.pprint(current_app.config['SQLALCHEMY_DATABASE_URI']) 
    pp.pprint(db)

# Factory to create the app
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    login.init_app(app)
    login.login_view = 'auth.login'

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # default config added here
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    # This config is not part of the git project but is created in the instance folder 
    # following Flask conventions of handling config
    app.config.from_pyfile('config.py')
    # Initialize SQLAlchemy 
    db.init_app(app)

    from todoapp import auth, tasks
    app.register_blueprint(auth.bp)
    app.register_blueprint(tasks.bp)
    app.add_url_rule("/", endpoint="tasks.index")

    return app
