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
        SECRET_KEY= os.urandom(16)
        #SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://<username>:<password>@<rds-instance-name>.us-west-2.rds.amazonaws.com/innodb'
        #SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    # Load the actual DB info from a config file outside of your git repo so that the 
    # access params for your RDS DB are not publicly exposed
    #configpath = os.environ['HOME']
    configpath = os.path.abspath(os.environ['TODOAPP_CONFIG'])
    print(configpath)    
    #filename = os.path.join(configpath,'todo_config.py')
    #print(filename)
    app.config.from_pyfile(configpath)
    
    # Initialize SQLAlchemy 
    db.init_app(app)

    from todoapp import auth, tasks
    app.register_blueprint(auth.bp)
    app.register_blueprint(tasks.bp)
    app.add_url_rule("/", endpoint="tasks.index")

    return app
