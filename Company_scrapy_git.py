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
    name = driver.find_element_by_css_selector(
        '#_container_baseInfo > table:nth-child(1) > tbody > tr:nth-child(1) > td.left-col.shadow > div > div:nth-child(1) > div.humancompany > div.name > a').text
    base_money = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(1) > td:nth-child(2) > div').text
    real_money = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(1) > td:nth-child(4)').text
    starting_date = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(2) > td:nth-child(2) > div').text
    business_statue = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(2) > td:nth-child(4)').text
    social_code = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(3) > td:nth-child(2)').text
    regist_code = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(3) > td:nth-child(4)').text
    tax_code = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(4) > td:nth-child(2)').text
    orgnization_code = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(4) > td:nth-child(4)').text
    company_type = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(5) > td:nth-child(2)').text
    industry = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(5) > td:nth-child(4)').text
    time = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(6) > td:nth-child(2)').text
    reg_orgnization = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(6) > td:nth-child(4)').text
    run_time = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(7) > td:nth-child(2) > span').text
    tax = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(7) > td:nth-child(4)').text
    employee = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(8) > td:nth-child(2)').text
    insurance = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(8) > td:nth-child(4)').text
    old_name = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(9) > td:nth-child(2)').text
    eng_name = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(9) > td:nth-child(4)').text
    adress = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(10) > td:nth-child(2)').text
    business = driver.find_element_by_css_selector(
        '#_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall > tbody > tr:nth-child(11) > td:nth-child(2) > span').text
    src=driver.page_source
    tyc_num = len(re.findall('tyc-num',src))
    target_font = ''
    target_font2 = ''
    try:
        font = driver.find_elements_by_tag_name('link')
        for i in font:
            href = i.get_attribute('href')
            if 'font' in href:
                target_font = href
    except:
        target_font = ''

    try:
            target_font2 = driver.find_element_by_css_selector('head > link:nth-child(47)').get_attribute('href')
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


def find_stuff_second_table(driver, company, list_name):
    second_result = pd.DataFrame(
        columns=['company', 'order', 'invested_company', 'representative', 'date', 'invests_amount', 'invests_portion',
                 'status', 'product', 'organization'])
    find_element = driver.find_elements_by_xpath('//*[@id="_container_invest"]/div/table/tbody/tr')
    for each_tr in find_element:
        td = each_tr.find_elements_by_xpath(".//td")
        order = td[0].text
        invested_company = td[1].find_element_by_xpath('.//a').text
        representative = td[4].find_element_by_xpath('.//a').text
        date = td[7].find_element_by_xpath('.//span').text
        invests_amount = td[8].find_element_by_xpath('.//span').text
        invests_portion = td[9].find_element_by_xpath('.//span').text
        status = td[10].find_element_by_xpath('.//span').text
        product = td[11].find_element_by_xpath('.//span').text
        organization = td[12].find_element_by_xpath('.//span').text
        data = {'company': company, 'order': order, 'invested_company': invested_company,
                'representative': representative, 'date': date,
                'invests_amount': invests_amount, 'invests_portion': invests_portion,
                'status': status, 'product': product, 'organization': organization, 'list_name': list_name}
        second_result = second_result.append(data, ignore_index=True)
    col = ['company', 'order', 'invested_company', 'representative', 'date', 'invests_amount', 'invests_portion',
           'status', 'product', 'organization', 'list_name']
    if len(second_result.index > 0):
        second_result = second_result[col]
    return second_result


def find_stuff_third_table(driver, company, list_name):
    third_result = pd.DataFrame()
    driver.execute_script("window.scrollTo(0, 300)")
    window_before = driver.window_handles[1]
    driver.find_element_by_xpath('//div[contains(@tyc-event-ch,"CompanyDetail.qiyetupu.Detail")]').click()
    WebDriverWait(driver, 3)
    window_after = driver.window_handles[2]
    driver.switch_to.window(window_after)

    iframe = driver.find_elements_by_tag_name('iframe')[0]
    driver.switch_to.frame(iframe)
    time.sleep(1)
    find_tag = driver.find_elements_by_tag_name('g')
    stock_owner_list = []
    employ_list = []
    hstock_owner = []
    invest_list = []
    branch_list = []
    hoper_list = []
    driver.find_element_by_css_selector('#graph-web-toolbar > ul > li:nth-child(3)').click()
    driver.find_element_by_css_selector('#graph-web-toolbar > ul > li:nth-child(3)').click()
    driver.find_element_by_css_selector('#graph-web-toolbar > ul > li:nth-child(3)').click()
    for each_tag in find_tag:
        if each_tag.get_attribute('class') == 'holder-node pointer':
            text_list = each_tag.find_elements_by_tag_name('text')
            text = ''
            for i in text_list:
                text = text + i.text + ','
            stock_owner_list.append(text)
        if each_tag.get_attribute('class') == 'executives-node pointer':
            text = ''
            for i in each_tag.find_elements_by_tag_name('text'):
                text = text + i.text + ','
            employ_list.append(text)
        if each_tag.get_attribute('class') == 'history-holder-node pointer':
            text = ''
            for i in each_tag.find_elements_by_tag_name('text'):
                text = text + i.text + ','
            hstock_owner.append(text)
        if each_tag.get_attribute('class') == 'invest-node pointer':
            text = ''
            for i in each_tag.find_elements_by_tag_name('text'):
                text = text + i.text + ','
            invest_list.append(text)
        if each_tag.get_attribute('class') == 'branch-node pointer':
            text = ''
            for i in each_tag.find_elements_by_tag_name('text'):
                text = text + i.text + ','
            branch_list.append(text)
        if each_tag.get_attribute('class') == 'hoper-node pointer':
            text = ''
            for i in each_tag.find_elements_by_tag_name('text'):
                text = text + i.text + ','
            hoper_list.append(text)
    # third_result_update = append_content(stock_owner_list, third_result, 'stock_owner', 'portion')
    # third_result_update = append_content(employ_list, third_result_update, 'employ', 'job')
    third_result_update = append_content_column(stock_owner_list, third_result, 'stock_owner')
    third_result_update = append_content_column(employ_list, third_result_update, 'employee')
    third_result_update = append_content_column(hstock_owner, third_result_update, 'hstock_owner')
    third_result_update = append_content_column(invest_list, third_result_update, 'invest')
    third_result_update = append_content_column(branch_list, third_result_update, 'branch')
    third_result_update = append_content_column(hoper_list, third_result_update, 'hoper')
    third_result_update['company'] = company
    third_result_update['list_name'] = list_name
    col = ['company', 'stock_owner', 'employee', 'hstock_owner', 'invest', 'branch', 'hoper', 'list_name']
    third_result_update = third_result_update[col]
    driver.close()
    driver.switch_to.window(window_before)
    driver.close()
    return third_result_update


def find_stuff_forth_table(driver, company, list_name):
    forth_result = pd.DataFrame(columns=['company', 'name', 'position', 'list_name'])
    tr = driver.find_elements_by_css_selector('#_container_staff > div > table > tbody > tr')
    for each_tr in tr:
        name = each_tr.find_elements_by_xpath('.//td[2]')
        name = name[-1].text
        position_1 = each_tr.find_elements_by_xpath('.//td[3]')
        position = position_1[-1].text
        data = {'company': company, 'name': name, 'position': position, 'list_name': list_name}
        forth_result = forth_result.append(data, ignore_index=True)
    return forth_result


def find_stuff_fifth_table(driver, company, list_name):
    fifth_result = pd.DataFrame(columns=['company', 'name', 'proportion', 'money', 'list_name'])
    tr = driver.find_elements_by_css_selector('#_container_holder > table > tbody > tr')
    for each_tr in tr:
        name = each_tr.find_element_by_xpath('.//td[2]/table/tbody/tr/td[2]/a').text
        proportion = each_tr.find_element_by_xpath('.//td[3]/div/div/span').text
        money = each_tr.find_element_by_xpath('.//td[4]/div/span').text

        data = {'company': company, 'name': name, 'proportion': proportion, 'money': money, 'list_name': list_name}
        fifth_result = fifth_result.append(data, ignore_index=True)
    return fifth_result


def find_stuff_sixth_table(driver, company, list_name):
    sixth_result = pd.DataFrame(columns=['company', 'brunch', 'represent', 'date', 'statue', 'list_name'])
    tr = driver.find_elements_by_css_selector('#_container_branch > table > tbody > tr')
    for each_tr in tr:
        brunch = each_tr.find_element_by_xpath('.//td[2]/table/tbody/tr/td[2]/a').text

        represent = each_tr.find_elements_by_xpath('.//td[3]')[0].text

        date = each_tr.find_element_by_xpath('.//td[4]/span').text

        statue = each_tr.find_element_by_xpath('.//td[5]/span').text

        data = {'company': company, 'brunch': brunch, 'represent': represent, 'date': date, 'statue': statue,
                'list_name': list_name}
        sixth_result = sixth_result.append(data, ignore_index=True)
    return sixth_result


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