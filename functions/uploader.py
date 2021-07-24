import owncloud
import os 

oc = owncloud.Client('https://drive.teamcodetech.in/')

EMAIL_ADDRESS = 'pancham@teamcodetech.in'
PASSWORD = 'Z12499840z#'
oc.login(EMAIL_ADDRESS, PASSWORD)


def upload(path, user, filename):
    try:
        oc.mkdir(user)
    except:
        pass
    oc.put_file(f'{user}/{filename}', f'{path}')
    os.remove(path)
    return True
