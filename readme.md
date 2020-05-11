A simple Todo app written in Python/Flask that lets users register and then login and create and delete ToDo tasks.

[Todo app hosted on AWS EC2 using ALB](http://todo-app-alb-487247043.us-west-2.elb.amazonaws.com/)


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
export TODOAPP_CONFIG=$HOME'/todo_config.py'
flask run
```
Run start.sh <br/>
Connect to [http://localhost:8080](http://localhost:8080)

## Database setup
This project uses MySQL as a database and uses SQLAlchemy package to extract out the DB info into an ORM so the underlying database can be switched as needed. You can add the following lines for setting up the DB in your $HOME/todo_config.py file for using a local db or AWS RDS instance. Config for dev vs prod will is covered later but the basic structure of connector url is shown below.
```python
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://<username>:<password>@<machine-name>/innodb'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```
Download MySQL Workbench to create the tables in the innodb database using the scripts in __dbcreate.sql__

# Project Setup
Main folder is called todo-project. Preferred dev IDE is __vscode__

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

![alt-text](https://github.com/shyam-eranky/todo-project/blob/master/img/vscode.jpg "VS code")

# Summary
This project uses multiple flask modules including flask for app creation and some common utilities, wtforms for encapsulating the different post/submit forms, flask-login which provides convenient classes for logging in users and managing sessions out of the box and Werkzeug for hashing password fields and verifying hashed passwords for login. The HTML templating is done using Jinja2 which is very JSP like and can be used to easily pass the class objects defined in the python files and iterate upon them.
## References
A lot of this code has been put together by referring to the following links which go into details of what each object does and how to use them. The code in this project is very simple and self explanatory but you can use the following links if you need more info.

[Flask mega tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

[Flask SQL Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

[Flask tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/)

# AWS Setup
## MySQL RDS setup
Follow the [AWS guide for MySQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.MySQL.html) to create a simple DB instance. The instance name you set is internal to AWS and is not used in any connection parameters you pass to your code. The default DB name (schema) is __innodb__. You can create a separate schema if you choose to. This example creates all tables in the innodb schema. 

_Remember to create a new __security group__ for this RDS instance. This project uses that security group for a) connecting using MySQL Workbench from my laptop and b) for allowing EC2 instances to connect to this RDS instance._

![alt-text](https://github.com/shyam-eranky/todo-project/blob/master/img/RDS1.jpg "RDS 1")

### Prod configuration for DB
There are multiple approaches to managing config per environment but this project uses a very simple approach of storing the DB params in a config file during EC2 instance creation and then modifying the envvars of apache2 also during instance creation to export a env var to point to this file. The code then reads this env var and then loads the config from the file. 

## EC2 instance creation
[Setup an EC2 instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html)
The EC2 setup is initiated by clicking the Launch Instance Wizard. Brief steps are outlined here
* Select the Ubuntu server AMI (as it comes with Python3 by default) with t2.micro free tier type and click Configure Instance details
* Select all the defaults for VPCs and subnets. You will need to select the CodeDeploy IAM role if you have already created it in the IAM role section. This is explained later. 
* In the User data section add the following script (see setup.txt file)
```python
#!/bin/bash
apt-get -y update
apt-get -y install ruby
apt-get -y install wget
apt-get -y install python3-pip
apt-get -y install apache2
apt-get -y install libapache2-mod-wsgi-py3 python-dev
# code deploy agent
cd /home/ubuntu
wget https://aws-codedeploy-us-west-2.s3.amazonaws.com/latest/install
chmod +x ./install
./install auto
# Setup flask dependencies
pip3 install flask
pip3 install flask-sqlalchemy
pip3 install mysql-connector-python
pip3 install flask-wtf 
pip3 install flask-login
#Apache config
chown -R ubuntu:ubuntu /var/www
chmod 2775 /var/www
find /var/www -type d -exec chmod 2775 {} \;
find /var/www -type f -exec chmod 0664 {} \;
chmod o+w /etc/apache2/sites-available/
echo -e "<VirtualHost *:80>\\nWSGIDaemonProcess todo threads=5\nWSGIProcessGroup todo\n WSGIScriptAlias / /var/www/html/todo-project/todo.wsgi\n<Directory /var/www/html/todo-project/static>\nOrder allow,deny\nAllow from all\n</Directory>\n</VirtualHost>" > /etc/apache2/sites-available/000-default.conf
echo -e "\nexport TODOAPP_CONFIG=/home/ubuntu/todo_config.py" >> /etc/apache2/envvars
 # Replace user pass and db name before you paste this in the userdata section of EC2 instance launch
echo -e "SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:pass@rdsname/innodb'\nSQLALCHEMY_TRACK_MODIFICATIONS = False" > /home/ubuntu/todo_config.py
```
* Select tags and add Name and unique value for CodeDeploy to identify this instance
* Create a new security group to allow http:80 and ssh:22 (from MyIp). This can be later changed when you add a load balancer. 
* Create a key pair and select it. Store the private key .pem file on your local laptop in a folder. This will be used to ssh to this instance when needed
![alt-text](https://github.com/shyam-eranky/todo-project/blob/master/img/ec2-1.jpg "EC2 1")
![alt-text](https://github.com/shyam-eranky/todo-project/blob/master/img/ec2-2.jpg "EC2 2")

### User Data explanation
The first section installs pip3 and apache2 and mod-wsgi which is used to run the web server in production.
Next we install the code deploy agent (see CodePipeline and CodeDeploy sections below). This agent is used to deploy the code
from Github onto the instance. Then we install all the python modules needed for this app including flask etc.
Finally we configure apache2 to host the webapp alongwith the wsgi config needed to point to the flask app. Also configure the 
actual params for connecting to your RDS MySQL instance here. This gets saved in a config file when instance is launched
and is used by the app to read the DB params. This way the DB params do not get exposed in Github.
## Load balancer and auto scaling group setup (coming soon)
* Create 3 security groups (lb-sg to allow all http traffic, app-sg for ec2 instances to allow http/80 from lb-sg, db-sg to allow mysql from app-sg)
* Create ELB
* Create Launch Template
* Create Autoscaling group , do not set the ELB check on it.
* Change CodeDeploy group to point to auto scaling group. Do not enable the Load Balancer option to block traffic and allow traffic as it doesnt work!
* Make sure lifecycle hook for code deploy gets added to your autoscale group

## Deployment from GitHub to EC2
Use CodeDeploy and CodePipeline in conjunction to setup deployment every time a commit is pushed onto master branch. 
[CodeDeploy](https://docs.aws.amazon.com/codedeploy/latest/userguide/getting-started-codedeploy.html)
[CodePipeline](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html#welcome-get-started)

Basic highlights :
* Setup an IAM role for CodeDeploy
* Setup an IAM role for EC2 instance profile
* A new IAM role will be created when you configure CodePipeline taking it to a total of 3 IAM roles!! 
* First configure the CodeDeploy app and add a deployment group by selecting the CodeDeployServiceRole and use the Name/value tags for Ec2 instances to let it know which EC2 instances to deploy to. Skip build stage for now.
* Create a new CodePipeline and let is create a new service role and select all other defaults. For Source select Github and connect to it. Then you can select the repo and master branch. For destination select the code deploy app you created above.
* Thats it! This will setup the github webhook in your github project. Each time a commit is pushed the pipeline gets triggered and it then calls the codedeploy job which then goes ahead and installs the app in /var/www/html on the ec2 instance and then restarts apache2. The appspec.yml file in your repo has the instructions for these steps.
![alt-text](https://github.com/shyam-eranky/todo-project/blob/master/img/deploy.jpg "deploy")

## Other AWS deployment options
These options are not suited for free tier but might be a better fit for real apps.
* [Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/)
* [ECS](https://aws.amazon.com/ecs/)
* [EKS](https://aws.amazon.com/eks/)
