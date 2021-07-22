from datetime import time
from flask import Flask, flash, request, session
from flask.templating import render_template
from pymongo.encryption import _DATA_KEY_OPTS
from werkzeug.utils import redirect
import bcrypt
from functions.users import check_existing_user, add_new_user, check_user_credentials
from functions.scheduler import add_medicine

app = Flask(__name__)
app.secret_key = 'subhogay'


@app.route('/')
def index():
    return render_template('index.html')


#Authentication
@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup/verify', methods=['GET', 'POST'])
def signup_verify():
    if request.method == 'POST':
        data = request.form
        name = data['name']
        email = data['email']
        password = data['password'].encode()
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        if not check_existing_user(email):
            add_new_user(name, email, hashed)
            flash('Registered')
            return redirect('/')
        else:
            flash('User with this email already exists.', 'error')
            return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/verify', methods=["GET", "POST"])
def login_verify():
    if request.method == "POST":
        data = request.form
        email = data['email']
        password = data['password']
        if check_user_credentials(email, password):
            session['user'] = email
            session['login'] = True
            flash('Logged in')
            return redirect('/')
        else:
            flash('Incorrect username or password!', 'error')
            return render_template('login.html')

#App Views
@app.route('/dashboard')
def dashboard():
    return render_template('app/dashboard.html')

#App Views
@app.route('/testing', methods=["GET", "POST"])
def testing():
    if request.method == "POST":
        session["user"] = 'adusharma22@gmial.com'
        data = request.form
        email = session["user"]
        medicine = data["medicine"]
        time = data["time"]
        days = data["days"]
        start = data["start"]
        end = data["end"]
        add_medicine(email, medicine, time, days, start, end)

    return render_template('testing.html')


@app.route('/schedule')
def schedule():
    return render_template('app/schedule.html')

@app.route('/settings')
def settings():
    return render_template('app/settings.html')

if __name__ == '__main__':
    app.run(debug=True)
