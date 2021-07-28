import smtplib
from email.mime.multipart import MIMEMultipart


EMAIL_ADDRESS = 'codetechbvn@gmail.com'
PASSWORD = ''


def sendmail(receiver, html):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Reminder - medSCHED"
    msg['From'] = 'codetechbvn@gmail.com'
    msg['To'] = receiver
    msg.attach(html)
    server.login(EMAIL_ADDRESS, PASSWORD)
    server.sendmail(EMAIL_ADDRESS, receiver, msg.as_string())
    server.quit()

