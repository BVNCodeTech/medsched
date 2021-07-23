from flask import session, flash
import owncloud


def connect():
    oc = owncloud.Client('https://drive.teamcodetech.in/')
    oc.login('pancham@teamcodetech.in', 'Z12499840z#')
    try:
        oc.mkdir('medSCHED')
    except:
        pass

def add_prescription():




