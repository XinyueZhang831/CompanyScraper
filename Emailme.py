import time
import smtplib
from email.mime.text import MIMEText
import os
import glob


def check_web(checking_path):
    file_length = len(glob.glob(checking_path))
    return file_length


def send_email(email_address, email_auth, send_content):
    mail_host = 'smtp.163.com'
    mail_user = 'xinyueamber'
    mail_pass = email_auth
    sender = email_address
    receivers = [email_address]
    message = MIMEText('sounds good', 'plain', 'utf-8')
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


class Emailme():
    def __init__(self, email_info):
        self.cp = email_info[0]
        self.ea = email_info[1]
        self.eau = email_info[2]
        self.sc = email_info[3]

    def Emailme(self):
        file_length = 0
        while True:
            file_length_1 = check_web(self.cp)
            if file_length == file_length_1:
                send_email(self.ea, self.eau, self.sc)
            else:
                file_length = file_length_1
            time.sleep(7200)
