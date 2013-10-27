from flask.ext.sqlalchemy import SQLAlchemy
from routes import Flask
from wtforms import Form, TextField, validators
import os

app = Flask(__name__)
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else: 
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/tdh' 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/tdh'
db = SQLAlchemy(app)    

class User(db.Model):
    name = db.Column(db.String(80))
    email = db.Column(db.String(80),primary_key=True)
    # do auth with fb or google instead
    password = db.Column(db.String(80))
    cost  = db.Column(db.String(80))
    frequency = db.Column(db.String(80))
    thingy = db.Column(db.String(80))

    def __repr__(self):
        return self.email
