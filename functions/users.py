from pymongo import MongoClient
import bcrypt
from flask import session

client = MongoClient(
    'mongodb+srv://pancham:pancham@niggaballs.tjmtx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client['medicine_schedule']
user_collection = db['users']
schedules = db['schedule']
prescriptions = db['prescriptions']


def check_existing_user(email):
    if user_collection.find_one({'_id': email.lower()}):
        return True
    else:
        return False


def add_new_user(name, email, password):
    user_collection.insert_one({
        '_id': email.lower(),
        'name': name,
        'password': password
    })
    schedules.insert_one({
        '_id':email.lower(),
        'medicines':{}
    })
    prescriptions.insert_one({
        '_id':email.lower(),
        'prescription':{}
    })


def check_user_credentials(email, password):
    user = user_collection.find_one({'_id': email.lower()})
    if user:
        return bcrypt.checkpw(password.encode(), user['password'])


def login_check():
    if session['login'] is True:
        return True
    else:
        return False
