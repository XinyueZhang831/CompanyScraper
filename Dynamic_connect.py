import os
import time
import subprocess

g_adsl_account = {"name": "宽带连接", "username": "051916769843","password": "657699"}


class Adsl(object):

# ==============================================================================
# __init__ : name: adsl名称
# ==============================================================================
    def __init__(self):
        self.name = g_adsl_account["name"]
        self.username = g_adsl_account["username"]
        self.password = g_adsl_account["password"]
# ==============================================================================
#  set_adsl : 修改adsl设置
# ==============================================================================
    def set_adsl(self, account):
        self.name = account["name"]
        self.username = account["username"]
        self.password = account["password"]
# ==============================================================================
#  connect : 宽带拨号
# ==============================================================================
    def connect(self):
        cmd_str = "rasdial %s %s %s" % (self.name, self.username, self.password)
        subprocess.call(cmd_str, shell=True)
        time.sleep(5)

# ==============================================================================
#  disconnect : 断开宽带连接
# ==============================================================================
    def disconnect(self):
        cmd_str = "rasdial %s /disconnect" % self.name
        subprocess.call(cmd_str, shell=True)
        time.sleep(5)
# ==============================================================================
# reconnect : 重新进行拨号
# ==============================================================================
    def reconnect(self):
        self.disconnect()
        self.connect()




