from flask import Flask, render_template, request, redirect, session, url_for, g
from functools import wraps
import requests, json
import models
import os
from flask_sslify import SSLify

app = Flask(__name__)
SSLify(app)

app.secret_key = "this_is_a_secret_key_for_testing"
if 'SECRET_KEY' in os.environ:
    app.secret_key = os.environ['SECRET_KEY']

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'email' in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def hello_world():
    return redirect('/login')

@app.route('/first')
def first():
    return render_template("first.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        session['email'] = request.form['email']
        session['password'] = request.form['password']

        response = requests.get("https://www.hackerschool.com/auth",
                            params={"email":session['email'], "password": session['password']})

        # check response status
        if response.status_code == 200:
            userinfo = json.loads(response.content)

            # does this person exist on the db
            myuser = models.User.query.filter_by(email=session['email']).first()

            if not myuser:

                u = models.User()
                u.email = session['email']
                models.db.session.add(u)
                models.db.session.commit()
                myuser = u
                # return "you're not in the db mofo but we added you"
                # start the session
                # go to the index page
            # return "valid login"

            return redirect(url_for('index'))

        else:
            # we should flash a message here
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/week/')
@login_required
def index():
    #get all the weeks
    w = models.Week.query.filter(models.Week.user_email == session['email']).all()
    return render_template("index.html", weeks=w)

@app.route('/week/new', methods=["POST", "GET"])
@login_required
def new_week():
    if request.method == "GET":
        return render_template("new_week.html")
    elif request.method == "POST":
        w = models.Week()
        w.number = int(request.form['number'])
        goal_number = int(request.form['goal_number'])
        w.user_email = session['email']
        models.db.session.add(w)
        models.db.session.commit()

        # create this num of pairings associated with this week
        # can probably be more db efficient
        for i in range(0, goal_number):
            p = models.Pairing()
            p.week_id = w.id
            p.done = False
            # Change me when we have users
            p.person = "Julie"
            models.db.session.add(p)
            models.db.session.commit()

        return render_template("week.html", week=w)
        # return "you want to pair " + str(goal_number) + "times!"
        # return "we posted some stuff"

## show a given week
## then show with its pairings
@app.route('/week/<id>')
@login_required
def show_week(id):
    w = models.Week.query.get(id)
    # how to et all the tasks
    mypairings = models.Pairing.query.filter(models.Pairing.week_id == w.id).all()
    return render_template("week.html", week=w, pairings=mypairings)

#FIXME need some code for not finding

@app.route('/week/<id>/pairing/<pair_id>', methods=["GET", "POST"])
@login_required
def show_pairing(id, pair_id):
    # w = models.Week.query.get(id)
    # how to et all the tasks
    # do we need the week id?
    p = models.Pairing.query.get(pair_id)
    # Worksheet.query??????
    return render_template("pairing.html", pairing=p)

@app.route('/week/<id>/pairing/<pair_id>/edit', methods=["GET", "POST"])
@login_required
def update_pairing(id, pair_id):
    # should check permissions somehoe!
    # get the form data
    if request.method == "GET":
        # does need to be by id as well?
        # not sure we need all these queries, we mostly just need the week id
        w = models.Week.query.get(id)
        p = models.Pairing.query.get(pair_id)
        return render_template("edit_pairing.html", week=w, pairing=p)

    elif request.method == "POST":
        p = models.Pairing.query.get(pair_id)
        p.person = request.form['person']
        done = request.form['done']
        # # return "Done is " + done
        if done == 'True':
            p.done = True
        else: p.done = False
        models.db.session.add(p)
        models.db.session.commit()
        return render_template("pairing.html", pairing=p)

if __name__ == '__main__':
    app.debug = True
    app.run()