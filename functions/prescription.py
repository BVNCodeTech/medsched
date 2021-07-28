import owncloud
import os
from flask import flash
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://pancham:pancham@niggaballs.tjmtx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client['medicine_schedule']
prescriptiondb = db['prescriptions']

# oc = owncloud.Client('https://drive.teamcodetech.in/')
# EMAIL_ADDRESS = 'pancham@teamcodetech.in'
# PASSWORD = ''
# oc.login(EMAIL_ADDRESS, PASSWORD)


def add_prescription(path=None, user=None, filename=None):
    try:
        oc.mkdir(f'medSCHED/{user}')
    except:
        pass
    try:
        oc.put_file(f'medSCHED/{user}/{filename}', path)
    except FileExistsError:
        pass
    os.remove(path)
    link = oc.share_file_with_link(f'medSCHED/{user}/{filename}').get_link()
    return link


def add_prescription_record(user, file_name, link):
    document = prescriptiondb.find_one({'_id':user.lower()})
    prescriptions = document['prescription']
    prescriptions[file_name] = link

    update = {'$set':{'prescription':prescriptions}}
    prescriptiondb.update_one({'_id':user.lower()}, update)
    return flash('Prescription uploaded')


def fetch_prescriptions(user):
    document = prescriptiondb.find_one({'_id':user.lower()})
    prescriptions = document['prescription']
    data = []
    count = 0
    for prescription in prescriptions:
        count +=1
        data.append({
            'name':prescription,
            'link':prescriptions[prescription]
        })
    return data, count


def prescription_card(prescription, href):
    card = f"""<div class="flex flex-col card rounded-lg my-5 p-3 shadow-md">
                  <p class="text-gray-800 my-3">{prescription.title()}</p>
                  <div class="flex">
                  <a href='{href}' target='_blank'>
                    <button class="bg-primary-blue-light text-white p-1 rounded-lg flex">
                      <i class="fas fa-external-link-alt mt-1.5 mx-1"></i>
                      <p class="mt-1 font-medium">View</p>
                    </button></a>
                  </div>
                </div>"""
    return card