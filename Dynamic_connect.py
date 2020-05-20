import os
import time
import subprocess

g_adsl_account = {"name": "宽带连接", "username": "051916769843","password": "657699"}


class Adsl(object):

    def __init__(self):
        self.name = g_adsl_account["name"]
        self.username = g_adsl_account["username"]
        self.password = g_adsl_account["password"]

    def set_adsl(self, account):
        self.name = account["name"]
        self.username = account["username"]
        self.password = account["password"]

    def connect(self):
        cmd_str = "rasdial %s %s %s" % (self.name, self.username, self.password)
        subprocess.call(cmd_str, shell=True)
        time.sleep(5)


    def disconnect(self):
        cmd_str = "rasdial %s /disconnect" % self.name
        subprocess.call(cmd_str, shell=True)
        time.sleep(5)

    def reconnect(self):
        self.disconnect()
        self.connect()




