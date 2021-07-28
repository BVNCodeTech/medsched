from functions.scheduler import fetch_user_schedule
from flask import session, flash
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(
    'mongodb+srv://pancham:pancham@niggaballs.tjmtx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
scheduledb = client['medicine_schedule']


def upcoming_notifications(user):
    data = fetch_user_schedule(datetime.now(), session['user'])
    now = str(datetime.now()).split('.')[0][-8:-3]
    data['current_time'] = now

    upcoming = {}

    data = dict(sorted(data.items(), key=lambda item: item[1]))

    upcoming_count = 0
    checkpoint = False
    for medicine in data:
        if medicine == 'current_time':
            checkpoint = True
        elif checkpoint:
            upcoming_count += 1
            upcoming[medicine] = data[medicine]
    return upcoming


def check_reminder_notification_method(user, upcoming):
    document = scheduledb.find_one({'_id': user.lower()})['medicines']
    notifications = {}
    for medicine in upcoming:
        if document[medicine]['mail']:
            notifications[medicine] = {'mail':True}
        else:
            notifications[medicine] = {'mail':False}
        if document[medicine]['whatsapp']:
            notifications[medicine]['whatsapp'] = True
        else:
            notifications[medicine]['whatsapp'] = False
    return notifications