from flask import Flask, flash, request
from flask.templating import render_template
from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key = 'subhogay'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        flash('N BALLS ')
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        print(first_name + last_name)
        return redirect('/')  

    return render_template('login.html')

@app.route('/med')
def meds():
    return 'Meds list'

app.run(debug=True)
