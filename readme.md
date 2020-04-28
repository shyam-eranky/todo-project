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
