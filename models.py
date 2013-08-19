from flask.ext.sqlalchemy import SQLAlchemy
from routes import Flask
# hmm does this go here?
# from flask_wtf import Form
# from wtforms import TextField, DataRequired
from wtforms import Form, TextField, validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class SignupForm(Form):
    name = TextField('Name', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = TextField('Password', [validators.Required()])


# # a boolean is it done
# # possibly associated with a given HS peeps if we can get into the HS auth
# class Pairing(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     done = db.Column(db.Boolean, default=False)
#     person = db.Column(db.String(80))
#     week_id = db.Column(db.Integer,db.ForeignKey('week.id'))
#
#     def __repr__(self):
#         return str(self.id)

# # represents the week of hacker school
# # have some function that maps the current date
# # to which week it is
# # need to change this to weekly_goal
# # hardcode helper function somehow.
# class Week(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     number = db.Column(db.Integer)
#     pairings = db.relationship('Pairing', backref='week', lazy='dynamic')
#     user_email = db.Column(db.Integer,db.ForeignKey('user.email'))
#
#     def __repr__(self):
#         return "Hacker School Week #" + str(self.number)

class User(db.Model):
    name = db.Column(db.String(80))
    email = db.Column(db.String(80), primary_key=True)
    # do auth with fb or google instead
    password = db.Column(db.String(80))
    cost  = db.Column(db.String(80))
    frequency = db.Column(db.String(80))
    thingy = db.Column(db.String(80))

    def __repr__(self):
        return self.email
# hmm does this go here?
#
# class MyForm(Form):
#     name = TextField(name, validators=[DataRequired()])