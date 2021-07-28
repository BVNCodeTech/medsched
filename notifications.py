from functions.notifications import *
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://pancham:pancham@niggaballs.tjmtx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client['medicine_schedule']
usersdb = db['users']



stop = []


def notifications(user):
    if user not in stop:
        upcoming = upcoming_notifications(user)
        if upcoming:
            notification = check_reminder_notification_method(user, upcoming)
            medicine = notification[0]
            email = notification[1]['mail']
            whatsapp = notification[2]['whatsapp']
            if email:
                send_email_notifications(user, notification)
            if whatsapp:
                contact, emergency_contact, name = get_user_contact(user)
                message = f"You have to take {medicine} right now"
                send_whatsapp_notifications(f"+91{contact}", message)
                message = f"{name} has to take {medicine} right now"
                send_whatsapp_notifications(f"+91{emergency_contact}", message)
        stop.append(user)
        print('checking for notifications')

users = []

results = usersdb.find()
if results:
    for result in results:
        users.append(result['_id'])

while True:
    for user in users:
        notifications(user)


