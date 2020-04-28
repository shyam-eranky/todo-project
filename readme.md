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
This project uses MySQL as a database and uses SQLAlchemy package to extract out the DB info into an ORM so the underlying database can be switched as needed. You can add the following lines for setting up the DB in your __init.py__ file for using a local db instance. If you want to connect to a prod instance hosted on AWS RDS then add these lines to a new file called config.py in the instance folder that gets created when you run the server once.
```python
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://<username>:<password>@<rds-instance-name>.us-west-2.rds.amazonaws.com/innodb'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```
Download MySQL Workbench to create the tables in the innodb database. 

# Project Setup

