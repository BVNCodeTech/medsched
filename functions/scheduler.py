from pymongo import MongoClient
from flask import session
import json


client = MongoClient(
    'mongodb+srv://pancham:pancham@niggaballs.tjmtx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client['medicine_schedule']
scheduledb = db['schedule']


# 5:20 AM
# 27-7-2021
def add_medicine(email, object: dict):
    document = scheduledb.find_one({'_id': email.lower()})
    medicine = object['medicine_name']
    del object['medicine_name']
    medicines = document['medicines']
    medicines[medicine] = object
    update = {'$set': {'medicines': medicines}}
    scheduledb.update_one({'_id': email.lower()}, update)


def edit_medicine(email, old_medicine_name, new_medicine_name):
    document = scheduledb.find_one({'_id': email.lower()})
    new = str(document).replace(old_medicine_name, new_medicine_name)
    new = new.replace("'", '"')
    new = json.loads(new)
    scheduledb.replace_one(document, new)

# WILL MAKE FUNCS TO EDIT OTHER PARAMETERS WHEN THEY ARE FINALISED AS DATETIME OBJECTS
