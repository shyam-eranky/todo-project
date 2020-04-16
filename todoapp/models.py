# Holds the ORM classes to represent the User and their ToDo tasks
from . import db, login
from sqlalchemy import func
from werkzeug.security import(check_password_hash,generate_password_hash)
from flask_login import UserMixin

# User class to represent the user and the FK many to one to the list of 
# ToDo tasks owned by the user
class User(UserMixin,db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(256),
                     index=False,
                     unique=True,
                     nullable=False)
    password = db.Column(db.String(1024),
                      nullable=False)
    email = db.Column(db.String(80),
                      index=True,
                      unique=True,
                      nullable=False)
    created = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=False,
                        default=func.now())
    tasks = db.relationship("ToDo", back_populates="user")

    def __init__(self, username,email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def serialize(self):
        return {"username": self.username,"email": self.email}


# ToDo class to represent each task and has the FK link back to the User object
# who owns this task
class ToDo(db.Model):
    __tablename__ = 'ToDo'
    id = db.Column(db.Integer,
                   primary_key=True)
    title = db.Column(db.String(256),
                     nullable=False)
    description = db.Column(db.String(80))
    created = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=False, default=func.now() )
    due = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    user = db.relationship("User", back_populates="tasks")
                    

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id

    def __repr__(self):
        return '<ToDo %r>' % self.title

    def serialize(self):
        return {"title": self.title,"user_id": self.user_id}

@login.user_loader
def load_user(id):
    return User.query.get(int(id))