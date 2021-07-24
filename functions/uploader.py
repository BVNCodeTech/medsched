import owncloud
import os 

oc = owncloud.Client('https://drive.teamcodetech.in/')

EMAIL_ADDRESS = 'aryan@teamcodetech.in'
PASSWORD = 'CTdabest@2021'
print('client made')
oc.login(EMAIL_ADDRESS, PASSWORD)

def upload(path, user, filename):
    print('function called')
    try:
        oc.mkdir(user)
    except:
        pass
    print('directory made')
    oc.put_file(f'{user}/{filename}', f'{path}')
    os.remove(path)
    return True
