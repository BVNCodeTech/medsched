from datetime import time
from flask import Flask, flash, request, session
from flask.templating import render_template
from werkzeug.utils import redirect, secure_filename
import bcrypt
from functions.users import check_existing_user, add_new_user, check_user_credentials
from functions.scheduler import add_medicine
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'subhogay'
app.config['UPLOAD_FOLDER'] = '/user_temporary_files'


@app.route('/')
def index():
    return render_template('index.html')


# Authentication
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
    try:
        if session['login']:
            return redirect('/dashboard')
        else:
            return render_template('login.html')
    except:
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
            return redirect('/dashboard')
        else:
            flash('Incorrect username or password!', 'error')
            return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    session['login'] = False
    session['user'] = None
    return redirect('/login')


# App Views
@app.route('/dashboard')
def dashboard():
    return render_template('app/dashboard.html')


@app.route('/schedule')
def schedule():
    return render_template('app/schedule.html')


@app.route('/schedule/add', methods=["GET", "POST"])
def add_schedule():
    return render_template('app/add-medicine.html')


@app.route('/schedule/submit', methods=['GET',"POST"])
def submit_schedule():
    data = request.form
    data = data.copy()
    dose_time = datetime.strptime(f"{data['hours']}:{data['minutes']} {data['halftime']}", '%I:%M %p')
    schedule_data = {
        'medicine_name':data['medicine-name'],
        'dose_time':dose_time.strftime("%H:%M:%S"),
        'start_date': datetime.strptime(data['start-date'].replace('-',''), '%Y%m%d'),
        'end_date':datetime.strptime(data['end-date'].replace('-',''), '%Y%m%d')
    }
#datetime.strptime(f"{data['hours']}:{data['minutes']} {data['halftime']}", '%I:%M %p')
    data['medicine-name']=None
    data['hours'] = None
    data['minutes'] = None
    data['halftime'] = None
    data['start-date'] = None
    data['end-date'] = None

    days = []
    for key in data:
        if data[key]:
            days.append(key)
    schedule_data['days'] = days
    add_medicine(session['user'], schedule_data)
    return redirect('/schedule')


@app.route('/prescription')
def prescription_view():
    pass


@app.route('/prescription/add')
def add_prescription():
    return render_template('app/add-prescription.html')


@app.route('/prescription/submit', methods=['GET','POST'])
def submit_prescription():
    data = request.form
    print(data)
    prescription_title = data.get('prescription-name')
    file = request.files['file']
    file.save(secure_filename(file.filename))



@app.route('/settings')
def settings():
    return render_template('app/settings.html')


if __name__ == '__main__':
    app.run(debug=True)
