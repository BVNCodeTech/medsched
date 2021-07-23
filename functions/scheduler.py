from pymongo import MongoClient
from flask import session
import json 

client = MongoClient(
    'mongodb+srv://pancham:pancham@niggaballs.tjmtx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client['medicine_schedule']
scheduledb = db['schedule']


def add_medicine(email, medicine, time, days, start, end):

    document = scheduledb.find_one({'_id':email.lower()})
    meds = str(document['medicines'])[:-1]  # to remove the last } from the dict
    new = '''{"_id":"%s", "medicines":%s,"%s":{"time":"%s","days_of_week":"%s","start":"%s","end":"%s"}}}''' % (email, meds, medicine, time, days, start, end) # makes a new dict and puts in the values we need into the already saved document, % formatting used because f strings wouldn't work
    res = new.replace("'", '"')
    res = json.loads(res)
    scheduledb.replace_one(document, res)


def edit_medicine(email, old_medicine_name, new_medicine_name):
    document = scheduledb.find_one({'_id':email.lower()})
    new = str(document).replace(old_medicine_name, new_medicine_name)
    new = new.replace("'", '"')
    new = json.loads(new)
    scheduledb.replace_one(document, new)

# WILL MAKE FUNCS TO EDIT OTHER PARAMETERS WHEN THEY ARE FINALISED AS DATETIME OBJECTS