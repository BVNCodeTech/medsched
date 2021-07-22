from flask import Flask, flash, request, session
from flask.templating import render_template
from werkzeug.utils import redirect
import bcrypt
from users import check_existing_user, add_new_user, check_user_credentials

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


@app.route('/schedule')
def schedule():
    return render_template('app/schedule.html')


@app.route('/medicines')
def medicines():
    return render_template('app/medicines.html')


@app.route('/prescriptions')
def prescriptions():
    return render_template('app/prescriptions.html')

@app.route('/settings')
def settings():
    return render_template('app/settings.html')

if __name__ == '__main__':
    app.run(debug=True)
