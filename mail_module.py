import smtplib as smtp
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

load_dotenv()


def mail_send(message, recipient):
    '''Sending mails.'''
    msg = MIMEMultipart()
    login = os.getenv('MAIL_LOGIN')
    password = os.getenv('MAIL_PASS')
    msg['From'] = login
    msg['To'] = recipient
    msg['Subject'] = 'Your order from Wildberries is ready to receive'
    body = message
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()

    server = smtp.SMTP_SSL('smtp.yandex.ru:465')
    server.login(login, password)

    server.sendmail(login, msg['To'], text)
