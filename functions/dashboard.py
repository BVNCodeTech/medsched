from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://pancham:pancham@niggaballs.tjmtx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client['medicine_schedule']
users = db['users']
scheduledb = db['schedule']


def user_name(user):
    document = users.find_one({"_id":user})
    return document['name']


def today_card(medicine, time):
    card = f"""<div class="card">
                  <div class="rounded-lg mx-8 my-3 bg-primary-blue-accent px-4 py-2" onclick="show_slideover()">
                    <p class="my-3 text-primary-blue-dark text-lg">{medicine.title()}</p>
                    <!-- Use jinja to enter medicine name here -->
                    <p class="my-3 text-primary-blue-dark text-lg">At {time}</p>
                  </div>
                  <!-- If it is the last card of the day then do not render the border -->
                  <div class="mt-3 border-t mx-8 border-gray-200 text-right"></div>
                </div>"""
    return card


def tomorrow_card(medicine, time):
    card = f"""<div class="card">
                  <div class="rounded-lg mx-8 my-3 bg-primary-green-light px-4 py-2">
                    <p class="my-3 text-primary-blue-dark text-lg">{medicine.title()}</p>
                    <!-- Use jinja to enter medicine name here -->
                    <p class="my-3 text-primary-blue-dark text-lg">At {time}</p>
                  </div>
                  <div class="mt-3 border-t mx-8 border-gray-200  text-right"></div>
                </div>"""
    return card


def day_after_card(medicine, time):
    card = f"""<div class="card">
                  <div class="rounded-lg mx-8 my-3 bg-primary-yellow-accent px-4 py-2">
                    <p class="my-3 text-primary-blue-dark text-lg">{medicine.title()}</p>
                    <!-- Use jinja to enter medicine name here -->
                    <p class="my-3 text-primary-blue-dark text-lg">At {time}</p>
                  </div>
                  <div class="mt-3 border-t mx-8 border-gray-200  text-right"></div>
                </div>"""
    return card
