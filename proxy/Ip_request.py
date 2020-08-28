import requests
import json
import socket

class IpRequesst:

    def __init__(self,num_ip = 0, ifnew=True, add_ip=True):
        self.n = ifnew
        self.ai = add_ip
        self.ni = num_ip

    def request_ip(self):
        try:
            if self.n == True:
                print('here')
                targetUrl = ''
                resp = requests.get(targetUrl)
                resp_dict = json.loads(resp.text)
                first = IpRequesst.check_white_list(self, resp_dict)
                if first == False:
                    pass
                else:
                    IpRequesst.add_to_whitelist(self, first)
                second = resp_dict['data'][0]
                ip = second['ip']
                port = str(second['port'])
                name = ip + ":" + port
                print(name)
                IpRequesst.save_new_ip(self, name)
            else:
                name = IpRequesst.original_ip(self)
            return name
        except:
            IpRequesst.request_ip(self)
       


    def add_to_whitelist(self,first):
        str1= ''
        reps = requests.get(str1 + first)
        return reps


    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP


    def check_white_list(delf, info):
        ip = False
        if "请添加白名单" in info['msg']:
            ip = info['msg'][6:]
        return ip


    def save_new_ip(self,ip):
        file = 'store_ip.txt'
        with open(file, 'w') as filetowrite:
            filetowrite.write(ip)
        filetowrite.close()

    def original_ip(self):
        file = open('store_ip.txt', 'r')
        ip = file.readline()
        file.close()
        return ip

    def give_me_ip(self):
        file = open('/Users/xinyue/PycharmProjects/web_scraping/proxy/' + str(self.ni) + '.txt', 'r')
        lines = file.readlines()
        split_ip = lines[0].split(':')
        proxy = split_ip[0]
        port = int(split_ip[1])
        name = lines[1].replace('\n','')
        password = lines[2].replace('\n','')
        return proxy, port,name,password

    def count_ip(self):
        account = open('/Users/xinyue/PycharmProjects/web_scraping/proxy/count_proxy.txt', 'r')
        account_count = account.readline()
        account.close()
        if self.ai:
            file = '/Users/xinyue/PycharmProjects/web_scraping/proxy/count_proxy.txt'
            with open(file, 'w') as filetowrite:
                filetowrite.write(str(int(account_count) + 1))
            filetowrite.close()
            account_return = str(int(account_count) + 1)
        else:
            account_return = str(account_count)
        return int(account_return)



#print(IpRequesst(True).add_to_whitelist())
#IpRequesst().add_to_whitelist()
