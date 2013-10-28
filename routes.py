from flask import Flask, render_template, flash, jsonify, request, redirect, session, url_for, g
from functools import wraps

from flask_wtf import Form
from wtforms import TextField, PasswordField, HiddenField, validators

from wtforms.validators import DataRequired
from flask.ext.bootstrap import Bootstrap

import models
import os
from flask_sslify import SSLify

app = Flask(__name__)
# SSLify(app)
Bootstrap(app)

### some stuff for bootstrap
app.config['BOOTSTRAP_USE_MINIFIED'] = True
app.config['BOOTSTRAP_USE_CDN'] = True
app.config['BOOTSTRAP_FONTAWESOME'] = True
app.config['SECRET_KEY'] = 'devkey'

app.secret_key = "this_is_a_secret_key_for_testing"
if 'SECRET_KEY' in os.environ:
    app.secret_key = os.environ['SECRET_KEY']

class SignupForm(Form):
    name = TextField('Name',validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired()])
    password = PasswordField('Password',
                       validators=[DataRequired()])
    submit_thingy = HiddenField('hidden_field')
    submit_cost = HiddenField('submit_cost')
    submit_frequency = HiddenField('submit_frequency')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'email' in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def hello_world():
    return redirect('/first')

@app.route('/first')
def first():
    form = SignupForm()
    return render_template("first.html", form=form)

@app.route('/signup', methods=["POST", "GET"])
def signup():
    print "IN SIGNUP"
    form = SignupForm()
    if request.method == "GET":
        return render_template("signup.html", form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            # check that user doesn't exist already
            email = form.email.data
            myuser = models.User.query.filter_by(email=email).first()

            if myuser:
                # TODO: this should be ajax?
                flash("Email already exists. Is that you? Sign in or choose different name.", 'error')
                return render_template("signup.html", form=form)

            else:
                # create the user
                u = models.User()
                u.name = form.name.data
                u.email = form.email.data
                u.password = form.password.data
                u.cost = form.submit_cost.data
                u.frequency = form.submit_frequency.data
                u.thingy = form.submit_thingy.data
                models.db.session.add(u)
                models.db.session.commit()
                # FIXME: can we redirect to login instead of doing it again?
                myuser = models.User.query.filter_by(email=u.email).first()
                # session['user'] = myuser
                session['email'] = u.email

                flash("Thanks for signing up!", 'success')

                return redirect(url_for('user'))

        else:
            flash("Form is not validating, how do we get right error?", "error")
            return render_template("signup.html", form=form)


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login2.html")

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # do we know this person?
        myuser = models.User.query.filter_by(email=email).first()

        # FIXME: what if myuser is null
        if myuser and myuser.password == password:
        # session['email'] = email
        # session['password'] = password
            # session['user'] = myuser
            session['email'] = email
            flash(u"You were successfully logged in.", 'success')
            return redirect(url_for('user'))

        else:
            # return "this user doesnt' exist"
            flash(u"Oops. Who are you? Did you misstype your password or username?", 'error')
            return render_template("login2.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route('/user')
def user():
    myuser = models.User.query.filter_by(email=session['email']).first()
    cost_per_use = float(myuser.cost) / float(myuser.frequency)
    cost_per_use = "%.2f" % cost_per_use
    return render_template("user.html", user=myuser, cost_per_use=cost_per_use)


@app.route('/update', methods=["POST"])
def update():
    email = session['email']
    myuser = models.User.query.filter_by(email=email).first()
    add_times = int(request.form['update_frequency'])
    # TODO verify is number
    times = int(myuser.frequency);
    new_frequency = times + add_times;
    myuser.frequency = new_frequency;
    models.db.session.add(myuser);
    models.db.session.commit();
    #FIXME: probably better way to do this
    cost_per_use = float(myuser.cost) / float(myuser.frequency)
    cost_per_use = "%.2f" % cost_per_use
    return render_template("user.html", user=myuser, cost_per_use=cost_per_use)
    # will this reflect the updated change

# # new ajaxy updated
# @app.route('/update', methods=["POST"])
# def update(add_frequency):
#     print "add frequency " + add_frequency
#     email = session['email']
#     myuser = models.User.query.filter_by(email=email).first()
#     add_times = add_frequency
#     # TODO verify is number
#     times = int(myuser.frequency);
#     new_frequency = times + add_times;
#     # should probs be an int to start
#     # return str(new_frequency);
#     myuser.frequency = new_frequency;
#     models.db.session.add(myuser);
#     models.db.session.commit();
#     # will this reflect the updated change
#     return new_frequency


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
