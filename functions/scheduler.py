from pymongo import MongoClient
from flask import session
import json
from datetime import datetime, date
import calendar

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


def fetch_user_schedule(user=None):
    document = scheduledb.find_one({'_id': user.lower()})
    medicines = document['medicines']
    med_dates = []
    for medicine in medicines:
        med_dates.append([medicine, medicines[medicine]['start_date'], medicines[medicine]['end_date']])

    today_meds = {}
    for med_date in med_dates:
        if datetime.now() < med_date[2]:
            today_meds[med_date[0]] = medicines[med_date[0]]['dose_time']
        else:
            pass
    return today_meds


def card(medicine, time):
    card_html = f"""<div class="flex flex-col card rounded-lg my-5 p-3 shadow-md">
                  <p class="text-gray-800 my-3">{medicine}</p>
                  <div class="flex">
                    <div class="bg-primary-blue-light text-white p-1 rounded-lg flex">
                      <object class="h-5 mr-1 mt-1" type="image/svg+xml" data="../../static/svg/clock.svg"></object>
                      <p class="mt-1 font-medium">{time} | {date.today()}</p>
                    </div>
                  </div>
                </div>"""
    return card_html
# WILL MAKE FUNCS TO EDIT OTHER PARAMETERS WHEN THEY ARE FINALISED AS DATETIME OBJECTS
