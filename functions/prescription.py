from flask import session, flash
import owncloud
from pymongo import MongoClient


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def connect():
    oc = owncloud.Client('https://drive.teamcodetech.in/')
    oc.login('pancham@teamcodetech.in', 'Z12499840z#')
    try:
        oc.mkdir('medSCHED')
    except:
        pass

def add_prescription():
    pass



