import time
import smtplib
from email.mime.text import MIMEText
import os
import glob
import json


def Email_me():
    values = json.load(open("setting_info.txt"))
    email_info = values[6]
    email_host = email_info[0]
    email_address = email_info[1]
    email_auth = email_info[2]
    send_content = email_info[3]
    parent_dir = os.getcwd() + '/'
    directory = '1'
    checking_path = parent_dir+directory

    file_length = 0
    while True:
        file_length_1 = check_web(checking_path)

        if file_length == file_length_1:
            send_email(email_host, email_address, email_auth, send_content)
        else:
            file_length = file_length_1
        time.sleep(7200)

def check_web(checking_path):
    file_length = len(glob.glob(checking_path))
    return file_length


def send_email(email_host, email_address, email_auth, send_content):
    mail_host = email_host
    mail_user = email_address
    mail_pass = email_auth
    sender = email_address
    receivers = [email_address]
    message = MIMEText(send_content, 'plain', 'utf-8')
    message['Subject'] = send_content
    message['From'] = sender
    message['To'] = receivers[0]
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print('error', e)



Email_me()