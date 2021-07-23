from pymongo import MongoClient
import json
import pytz


IST = pytz.timezone('Asia/Kolkata')


client = MongoClient(
    'mongodb+srv://pancham:pancham@niggaballs.tjmtx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client['medicine_schedule']
scheduledb = db['schedule']



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


def fetch_user_schedule(day, user=None):
    document = scheduledb.find_one({'_id': user.lower()})
    medicines = document['medicines']
    med_dates = []
    for medicine in medicines:
        med_dates.append([medicine, medicines[medicine]['start_date'], medicines[medicine]['end_date']])

    today_meds = {}
    for med_date in med_dates:
        if day < med_date[2]:
            today_meds[med_date[0]] = medicines[med_date[0]]['dose_time'][:-3]
        else:
            pass
    return today_meds


def no_data_check(user):
    document = scheduledb.find_one({"_id":user.lower()})
    medicines = document['medicines']
    if not medicines:
        return True
    else:
        return False


def card(medicine:str, time):
    card_html = f"""<div class="flex flex-col card rounded-lg my-5 p-3 shadow-md">
                  <p class="text-gray-800 my-3">{medicine.title()}</p>
                  <div class="flex">
                    <div class="bg-primary-blue-light text-white p-1 rounded-lg flex">
                      <i class="fas mt-1.5 mx-1 fa-clock"></i>
                      <p class="mt-1 font-medium">{time}</p>
                    </div>
                  </div>
                </div>"""
    return card_html
# WILL MAKE FUNCS TO EDIT OTHER PARAMETERS WHEN THEY ARE FINALISED AS DATETIME OBJECTS
