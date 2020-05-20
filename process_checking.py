import time
import smtplib
from email.mime.text import MIMEText
import os

def count_time():
    while True:
        testing_list = []
        t_end = time.time()+60*2
        while time.time()< t_end:
            if check_web():
                print('it break')
                testing_list.append('True')
                break
            else:
                print('False')
                testing_list.append('False')

        if 'True' not in testing_list:
            send_email()
        time.sleep(7200)


def check_web():
    name = 'ChromeDriver.exe'
    name_2 = 'chrome.exe'
    tmp = os.popen("tasklist").read()
    if (name in tmp) | (name_2 in tmp):
        return True
    else:
        print('finish searching')
        return False


def send_email():
    server = '20041 first machine'
    mail_host = 'smtp.163.com'
    mail_user = 'xinyueamber'
    mail_pass = 'FBSAGUYNPMNOXPOY'
    sender = 'xinyueamber@163.com'
    receivers = ['xinyuecheol@gmail.com']
    message = MIMEText('content', 'plain', 'utf-8')
    message['Subject'] = 'Server needs to reset:' + server
    message['From'] = sender
    message['To'] = receivers[0]
    print('here')
    try:
        smtpObj = smtplib.SMTP()
        print('here')
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error', e)


if __name__ == "__main__":
    count_time()
