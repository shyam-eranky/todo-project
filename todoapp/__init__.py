# Initialization of the todoapp module happens here
# Main flask app gets created using factory and the db ORM is setup
import os, sys
import pprint as pp
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Setup DB
db = SQLAlchemy()
login = LoginManager()

# Factory to create the app
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    login.init_app(app)
    login.login_view = 'auth.login'

    # ensure the instance folder exists
    #try:
    #    os.makedirs(app.instance_path)
    #except OSError:
    #    pass

    # default config added here
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://user:pass@localhost/innodb',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Load the actual DB info from a config file outside of your git repo so that the 
    # access params for your RDS DB are not publicly exposed
    configpath = os.path.abspath(os.environ['TODOAPP_CONFIG'])
    #sys.stderr.write(str(configpath)+ '\n')    
    app.config.from_pyfile(configpath)
    #sys.stderr.write(str(app.config['SECRET_KEY'])+ '\n')
    #sys.stderr.write(str(app.config['SQLALCHEMY_DATABASE_URI'])+ '\n')
    
    # Initialize SQLAlchemy 
    db.init_app(app)

    from todoapp import auth, tasks
    app.register_blueprint(auth.bp)
    app.register_blueprint(tasks.bp)
    app.add_url_rule("/", endpoint="tasks.index")

    return app
