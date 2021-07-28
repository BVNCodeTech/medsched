from functions.scheduler import fetch_user_schedule
from pymongo import MongoClient
from datetime import datetime
from email.mime.text import MIMEText
from functions.mailer import sendmail
from twilio.rest import Client

client = MongoClient(
    'mongodb+srv://pancham:pancham@niggaballs.tjmtx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client['medicine_schedule']
scheduledb = db['schedule']
users = db['users']

twilio_client = Client('', '')


def upcoming_notifications(user):
    data = fetch_user_schedule(datetime.now(), user)
    now = datetime.now()
    now = str(now).split('.')[0][-8:-3]

    data['current_time'] = now
    data = dict(sorted(data.items(), key=lambda item: item[1]))
    upcoming = None
    checkpoint = False
    for medicine in data:
        if medicine == 'current_time':
            checkpoint = True
        elif checkpoint:
            break
        else:
            upcoming = [medicine, data[medicine]]
    if upcoming[1] == now:
        return upcoming
    else:
        return None


def check_reminder_notification_method(user, upcoming):
    document = scheduledb.find_one({'_id': user.lower()})['medicines']
    notification = [upcoming[0]]
    try:
        if 'mail' in document[upcoming[0]]['notification']:
            notification.append({'mail': True})
        else:
            notification.append({'mail': False})
    except KeyError:
        notification.append({'mail': False})
    try:
        if 'whatsapp' in document[upcoming[0]]['notification']:
            notification.append({'whatsapp': True})
        else:
            notification.append({'whatsapp': False})
    except KeyError:
        notification.append({'whatsapp': False})
    return notification


def send_email_notifications(user, notification):
    mail_content = f"<h2>You have to take {notification[0]}<h2>"
    html = MIMEText(mail_content, 'html')
    sendmail(user.lower(), html)
    return None


def send_whatsapp_notifications(whatsapp_number, msg, media=None):
    to_whatsapp_number = 'whatsapp:' + whatsapp_number
    from_whatsapp_number = 'whatsapp:+14155238886'
    if not media:
        twilio_client.messages.create(body=msg,
                               from_=from_whatsapp_number,
                               to=to_whatsapp_number)
    else:
        twilio_client.messages.create(body=msg,
                               media_url=media,
                               from_=from_whatsapp_number,
                               to=to_whatsapp_number)


def get_user_contact(user):
    document = users.find_one({'_id':user.lower()})
    return document['contact'], document['emergency_contact'], document['name']