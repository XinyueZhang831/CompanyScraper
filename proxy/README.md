### Ip_request.py

Can be used to request new proxy from a proxy provider. 

open_ip will need change to 

```
    IP,PORT = get_new_IP()
    string_proxy= IP+ ':'+PORT
    string_part = '--proxy-server=http://'
    change_IP = string_part + string_proxy
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(change_IP)
    driver = webdriver.Chrome(executable_path='/chromedriver',options=chrome_options)

```



### proxy.py

Combine with Ip_request.py, this code can be use for proxy with authorization. it will be an extension added to the chromedriver extension.

open_ip will need change to 

```
    proxy_count = IpRequesst(add_ip=on).count_ip()
    num_proxy = proxy_count% 10
    print("+numer of proxy "+ str(num_proxy)+'+')
    #num_proxy =1
    host, port,username,password = IpRequesst(num_ip = num_proxy).give_me_ip()
    print(host)
    driver = proxy_chrome(host, port, username, password)
```
