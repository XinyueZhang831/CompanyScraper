import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from Comp_num import *
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from Dynamic_connect import *
import re
import time
import socket


def open_ip(dynamic=False):
    if dynamic:
        print(get_ip())
        Adsl().disconnect()
        time.sleep(2)
        Adsl().connect()
        print(get_ip())
        time.sleep(5)
    else:
        Adsl().connect()
        print(get_ip())
        time.sleep(2)


    driver = webdriver.Chrome(executable_path= os.getcwd()+'/driver/chromwebdriver')
    driver.get('This is website')
    driver.implicitly_wait(2)
    check = check_the_site(driver)
    while check == False:
        time.sleep(1)
        driver = quit_driver(driver)
        open_ip(log_in=False, dynamic = True)
    start_scrape(driver)


def start_scrape(driver):
    parent_path = os.getcwd()
    num = CompNum(update=False).give_num()
    print(num)
    input_comp = pd.read_csv(os.getcwd()+'/sample.csv')[num:]
    for i, r in input_comp.iterrows():
        if type(r['company_name']) != float:
            print('*****start*****')
            try:
                driver = check_handels(driver)
                first_result, second_result, forth_result, fifth_result, sixth_result = search_comp(driver,
                                                                                                    r['company_name'])
                first_result.to_csv(
                    parent_path+'/1' + r['company_name'] + '.csv')
                second_result.to_csv(
                    parent_path+'/2' + r['company_name'] + '.csv')
                forth_result.to_csv(
                    parent_path+'/4' + r['company_name'] + '.csv')
                fifth_result.to_csv(
                    parent_path + '/5' + r['company_name'] + '.csv')
                sixth_result.to_csv(
                    parent_path+'/6' + r['company_name'] + '.csv')

                print('**finish -' + str(CompNum(update=False, num=i).give_num()) + '-')
                CompNum(update=True, num=i).give_num()
            except:
                print('==exception happen in this company: ' + str(i) + '==')
                driver.refresh()
        else:
            print('==Wrong comp name==')


def search_comp(driver, comp_name):
    try:
        driver.implicitly_wait(2)
        check_second_robort(driver)
        driver.find_element_by_id('header-company-search').clear()
        inputElement = driver.find_element_by_id("header-company-search")
        inputElement.send_keys(comp_name)
        inputElement.send_keys(Keys.ENTER)

        check_second_robort(driver)
        check_return_info(driver)
        company_link = driver.find_elements_by_class_name('name')
        window_before = driver.window_handles[0]
        driver.execute_script("arguments[0].click();", company_link[0])

        # check_robort(driver)
        check_second_robort(driver)
        check_return_info(driver)
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        check_return_info(driver)
       # time.sleep(20000)
        # check_return_info(driver)
        current_name = driver.find_element_by_css_selector('div.header > h1').text
        first_result, second_result, forth_result, fifth_result, sixth_result = scrape_info(driver, current_name,
                                                                                            comp_name)
        # first_result, second_result, third_result= scrape_info(driver,current_name, comp_name, num)
        driver.close()
        # driver = check_handels(driver)
        driver.switch_to.window(window_before)
        # return first_result, second_result, third_result
        return first_result, second_result, forth_result, fifth_result, sixth_result
    except:
        print('=+=Wait time too long=+=')
        driver.refresh()
        driver=quit_driver(driver)
        open_ip(dynamic=True)


def scrape_info(driver, current_name, comp_name):
    try:
        first_result = find_stuff_first_table(driver, current_name, comp_name)
    except:
        first_result = pd.DataFrame()
    #time.sleep(20000)
    try:
        second_result = find_stuff_second_table(driver, current_name, comp_name)
    except:
        second_result = pd.DataFrame()
    try:
        forth_result = find_stuff_forth_table(driver, current_name, comp_name)
    except:
        forth_result = pd.DataFrame()
    try:
        fifth_result = find_stuff_fifth_table(driver, current_name, comp_name)
    except:
        fifth_result = pd.DataFrame()
    try:
        sixth_result = find_stuff_sixth_table(driver, current_name, comp_name)
    except:
        sixth_result = pd.DataFrame()
    # try:
    #    third_result = find_stuff_third_table(driver, current_name, comp_name)
    # except:
    #    third_result = pd.DataFrame()
    # return first_result, second_result, third_result
    return first_result, second_result, forth_result, fifth_result, sixth_result


def find_stuff_first_table(driver, current_name, comp_name):
    first_table = pd.DataFrame(
        columns=['name', 'base_money', 'real_money', 'starting_date', 'business_statue', 'social_code', 'regist_code',
                 'tax_code', 'orgnization_code', 'company_type',
                 'industry', 'time', 'reg_orgnization', 'run_time', 'tax', 'employee', 'insurance', 'old_name',
                 'eng_name', 'adress', 'business', 'list_name', 'comp_name','tyc-num','font','font2'])
    name = driver.find_element_by_css_selector().text
    base_money = driver.find_element_by_css_selector().text
    real_money = driver.find_element_by_css_selector().text
    starting_date = driver.find_element_by_css_selector().text
    business_statue = driver.find_element_by_css_selector().text
    social_code = driver.find_element_by_css_selector().text
    regist_code = driver.find_element_by_css_selector().text
    tax_code = driver.find_element_by_css_selector().text
    orgnization_code = driver.find_element_by_css_selector().text
    company_type = driver.find_element_by_css_selector().text
    industry = driver.find_element_by_css_selector().text
    time = driver.find_element_by_css_selector().text
    reg_orgnization = driver.find_element_by_css_selector().text
    run_time = driver.find_element_by_css_selector().text
    tax = driver.find_element_by_css_selector().text
    employee = driver.find_element_by_css_selector().text
    insurance = driver.find_element_by_css_selector().text
    old_name = driver.find_element_by_css_selector().text
    eng_name = driver.find_element_by_css_selector().text
    adress = driver.find_element_by_css_selector().text
    business = driver.find_element_by_css_selector().text
    src=driver.page_source
    tyc_num = len(re.findall('txx-num',src))
    target_font = ''
    try:
        font = driver.find_elements_by_tag_name('link')
        for i in font:
            href = i.get_attribute('href')
            if 'font' in href:
                target_font = href
    except:
        target_font = ''

    try:
            target_font2 = driver.find_element_by_css_selector('').get_attribute('href')
    except:
            target_font2 = ''
    data = {'name': name, 'base_money': base_money, 'real_money': real_money, 'starting_date': starting_date,
            'business_statue': business_statue, 'social_code': social_code, 'regist_code': regist_code,
            'tax_code': tax_code, 'orgnization_code': orgnization_code, 'company_type': company_type,
            'industry': industry, 'time': time, 'reg_orgnization': reg_orgnization, 'run_time': run_time, 'tax': tax,
            'employee': employee, 'insurance': insurance, 'old_name': old_name, 'eng_name': eng_name, 'adress': adress,
            'business': business, 'list_name': comp_name, 'comp_name': current_name,'tyc-num':tyc_num, 'font': target_font, 'font2':target_font2}
    first_table = first_table.append(data, ignore_index=True)
    return first_table





def append_content_column(waiting_list, df, var1):
    i = 0
    while i < len(waiting_list):
        df.at[i, var1] = waiting_list[i]
        i = i + 1
    if len(waiting_list) < 1:
        df.at[0, var1] = None
    return df


def check_handels(driver):
    if len(driver.window_handles) > 1:
        num = CompNum(update=False).give_num()
        print('*handle error*')
        print('-current is:' + str(num) + '-')
        handles = driver.window_handles
        for i in handles[1:]:
            driver.switch_to_window(i)
            driver.close()
        driver.switch_to_window(handles[0])
    return driver


def check_second_robort(driver):
    time.sleep(2)
    try:
        driver.implicitly_wait(3)
    except TimeoutException as e:
        print('===Wait too Long===')
        driver = quit_driver(driver)
        open_ip(dynamic = True)
    try:
        if driver.find_element_by_css_selector(
                '#web-content > div > div.container > div > div > div.module.module1.module2.loginmodule.collapse.in > div.scan-box > div.scan-wrapper > div.scan-img > img'):
            print('*log_in error*')
            num = CompNum(update=False).give_num()
            print('-current is:' + str(num) + '-')
            driver = quit_driver(driver)
            open_ip(log_in=False, dynamic = True)
    except:
        pass


def check_the_site(driver):
    src = driver.page_source
    text_found = re.search(r'ERR_EMPTY_RESPONSE', src)
    text_found_2 = re.search(r'The connection was reset', src)
    text_found_3 = re.search(r'took too long to respond.', src)
    if (text_found != None) | (text_found_2 != None) | (text_found_3 != None):
        return False
    else:
        return True


def check_return_info(driver):
    src = driver.page_source
    text_found = re.search(r'抱歉，该信息暂不予显示，查一查其它信息', src)
    text_found_1 = re.search(r'抱歉，没有找到相关企业！', src)
    text_found_2 = re.search(r'很抱歉', src)
    if (text_found != None) | (text_found_1 != None)|(text_found_2 != None):
        num = CompNum(update=False).give_num()
        CompNum(update=True, num = num).give_num()
        print('++ This company info is hide++')
        driver = quit_driver(driver)
        open_ip(dynamic=False)
    else:
        pass


def quit_driver(driver):
    driver.delete_all_cookies()
    driver.quit()
    subprocess.call("taskkill /F /IM ChromeDriver.exe", shell=True)
    subprocess.call("taskkill /F /IM chrome.exe", shell=True)
    print('quit sucessed')
    time.sleep(1)
    return driver

def get_ip():
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

if __name__ == "__main__":
    # execute only if run as a script
    open_ip()