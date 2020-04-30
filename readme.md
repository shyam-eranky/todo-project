# Development environment instructions
## Python and Flask dependencies setup
It is recommended to use a virtual env for installing Python3 and all its dependencies but that is not covered in this tutorial. Install Python3 (3.6 or higher is preferred) and pip3
```python
pip3 install flask
pip3 install flask-sqlalchemy
pip3 install mysql-connector-python
pip3 install flask-wtf 
pip3 install flask-login
```

## Run flask server in dev mode
```python
#!/bin/bash
export FLASK_APP=todo.py
export FLASK_ENV=development
export FLASK_DEBUG=1
export FLASK_RUN_PORT=8080
flask run
```
Run start.sh <br/>
Connect to [http://localhost:8080](http://localhost:8080)

## Database setup
This project uses MySQL as a database and uses SQLAlchemy package to extract out the DB info into an ORM so the underlying database can be switched as needed. You can add the following lines for setting up the DB in your __init.py__ file for using a local db instance. If you want to connect to a prod instance hosted on AWS RDS then add these lines to a new file called __config.py__ in the __instance__ folder that gets created when you run the server once.
```python
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://<username>:<password>@<rds-instance-name>.us-west-2.rds.amazonaws.com/innodb'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```
Download MySQL Workbench to create the tables in the innodb database using the scripts in __dbcreate.sql__

# Project Setup
Main folder is called todo-project.

|- todo.py : main python file todo.py which is used to create the Flask app

|- todo.wsgi : used to run the server in production mode using apache2 which is covered in a later section below

|- .gitignore : Use vscode extension to generate it for python and flask

|- setup.txt : Compilation of useful commands needed for EC2 setup covered later

|- start.sh : setup and run the flask local dev server on your localhost

|- todoapp : Folder containing all the application related code

...|- static : Contains the css and client side js assets
   
...|- templates : HTML Jinja2 snippets with base.html being the base file included in all the other files.
   
...|- __init__.py : Initializes the db and login manager and provides the factory to create the flask app
   
...|- forms.py : Holds the class definitions for login, register and tasks forms used by the front end
   
...|- models.py : SQLAlchemy based classes to model User and ToDo tasks for the user
   
...|- auth.py : Blueprint for the authentication code to handle login/logout/register
   
...|- tasks.py : Blueprint for the tasks code to handle create/delete of todo tasks for each user

# Summary
This project uses multiple flask modules including flask for app creation and some common utilities, wtforms for encapsulating the different post/submit forms, flask-login which provides convenient classes for logging in users and managing sessions out of the box and Werkzeug for hashing password fields and verifying hashed passwords for login. The HTML templating is done using Jinja2 which is very JSP like and can be used to easily pass the class objects defined in the python files and iterate upon them.
## References
A lot of this code has been put together by referring to the following two links which go into details of what each object does and how to use them. The code in this project is very simple and self explanatory but you can use the following links if you need more info.

[Flask mega tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

[Flask SQL Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

[Flask tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/)

# AWS Setup
## MySQL RDS setup
Follow the [AWS guide for MySQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.MySQL.html) to create a simple DB instance. The instance name you set is internal to AWS and is not used in any connection parameters you pass to your code. The default DB name (schema) is __innodb__. You can create a separate schema if you choose to. This example creates all tables in the innodb schema. 

_Remember to create a new __security group__ for this RDS instance. This project uses that security group for a) connecting using MySQL Workbench from my laptop and b) for allowing EC2 instances to connect to this RDS instance._



