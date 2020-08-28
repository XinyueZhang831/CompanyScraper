from PIL import Image,ImageGrab
from io import BytesIO
from selenium.webdriver.common.action_chains import ActionChains
import random
import time
from selenium.webdriver.support.ui import WebDriverWait
import re
from Account import *
#from Comp_nologin import*


class Login:
    def __init__(self,driver):
        self.driver = driver

    def login(self, up_date):
        #print('initial login')
        trying = self.driver.find_elements_by_class_name('nav-item ')
        WebDriverWait(self.driver,2)
        Account(up_date).count_account()
        try:
            i = 0
            for each in trying:
                i = i+1
                if each.text == '登录/注册':
                    each.click()
                    password_login = self.driver.find_elements_by_xpath('//div[contains(@class, "title")]')
                    for each_link in password_login:
                        if each_link.get_attribute('onclick') == 'loginObj.changeCurrent(1);':
                            each_link.click()
                            #print('start login')
                            time.sleep(1)
                            Login.login_with_password(self, up_date)
                            return self.driver
            #print(i)
            #if i ==len(trying):
                #time.sleep(1)
                #self.driver.refresh()
                #Login.login(self, False)
        except:
            self.driver.refresh()
            Login.login(self, False)


    def login_with_password(self,add_account):
        account = Account(add_account = add_account).count_account()
        #print(account+'-')
        num_account = int(account) % 6
        account_numb = Account(num_account=num_account).give_me_account()
        inputElement = self.driver.find_elements_by_tag_name('input')
        input_username = self.driver.find_element_by_css_selector('#mobile')
        input_username.send_keys(account_numb)
        input_passwoard = self.driver.find_element_by_css_selector('#password')
        input_passwoard.send_keys('Exo983106(*')
        try:
            text_found = None
            i = 0
            while text_found == None:
                i = i + 1
                self.driver.find_element_by_css_selector(
                    'div > div.body.-scorll-fix.modal-scroll > div > div > div.module.module1.module2.loginmodule.collapse.in > div.sign-in > div.modulein.modulein1.mobile_box.f-base.collapse.in > div.btn.-xl.btn-primary.-block').click()
                src = self.driver.page_source
                time.sleep(1)
                text_found = re.search(r'请先完成下方验证', src)
                time.sleep(1)
                if i == 5:
                    self.driver.refresh()
                    #print('inside the login_with_password')
                    Login.login(self, False)
            Login.autologin(self)
        except:
            time.sleep(3)
            driver = Login.autologin(self)
            return driver

    def autologin(self):

        time.sleep(2)
        img = self.driver.find_element_by_css_selector(
            'body > div.gt_holder.gt_popup.gt_show > div.gt_popup_wrap > div.gt_popup_box > div.gt_widget > div.gt_box_holder > div.gt_box > a.gt_fullbg.gt_show')
        time.sleep(0.5)

        location = img.location

        size = img.size


        top, bottom, left, right = location['y'] - 300 + 30, location['y'] - 300 + 30 + size['height'] * 2, location[
            'x'] + 600, location['x'] + 550 + size[
                                       'width'] + 300 - 20

        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        captcha1 = screenshot.crop((left, top, right, bottom))

        captcha1.save('captcha1.png')

        self.driver.find_element_by_css_selector(
            'body > div.gt_holder.gt_popup.gt_show > div.gt_popup_wrap > div.gt_popup_box > div.gt_slider > div.gt_slider_knob.gt_show').click()
        time.sleep(4)
        img1 = self.driver.find_element_by_css_selector(
            'body > div.gt_holder.gt_popup.gt_show > div.gt_popup_wrap > div.gt_popup_box > div.gt_widget > div.gt_box_holder > div.gt_box > a.gt_fullbg.gt_hide > div.gt_cut_fullbg.gt_show')
        time.sleep(0.5)
        location1 = img1.location
        size1 = img1.size
        top1, bottom1, left1, right1 = location1['y'] - 300 + 30, location1['y'] - 300 + 30 + size1['height'] * 2, \
                                       location1['x'] + 600, location1['x'] + 550 + size1[
                                           'width'] + 300 - 20
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        captcha2 = screenshot.crop((left1, top1, right1, bottom1))
        captcha2.save('captcha2.png')

        left = 55

        for i in range(left, captcha1.size[0]):
            for j in range(captcha1.size[1]):

                pixel1 = captcha1.load()[i, j]
                pixel2 = captcha2.load()[i, j]
                f = open("pixel1.txt", "a+")
                f.write("pixel1 %s\r\n" % str(pixel1))
                f.close()
                f1 = open("pixel2.txt", "a+")
                f1.write("pixel2 %s\r\n" % str(pixel2))
                f1.close()
                threshold = 65
                if (abs(pixel1[0] - pixel2[0]) < threshold) & (abs(pixel1[1] - pixel2[1]) < threshold) & (
                        abs(pixel1[2] - pixel2[2]) < threshold):
                    pass
                else:
                    left = i


        Login.start_move(self,left)



    def start_move(self, distance):
        if distance>325:
            distance = distance+35
        element = self.driver.find_element_by_css_selector(
            'body > div.gt_holder.gt_popup.gt_show > div.gt_popup_wrap > div.gt_popup_box > div.gt_slider > div.gt_slider_knob.gt_show')
        distance -= element.size.get('width')
        distance = 6 * 23 * distance / (49 * 7)
        ActionChains(self.driver).click_and_hold(element).perform()
        time.sleep(0.5)
        while distance > 0:
            if distance > 10:

                span = random.randint(5, 8)
            else:

                span = random.randint(2, 3)
            ActionChains(self.driver).move_by_offset(span, 0).perform()
            distance = distance - span
        ActionChains(self.driver).move_by_offset(2, 0).perform()
        ActionChains(self.driver).pause(0.5).release().perform()
        try:
            time.sleep(3)
            if self.driver.find_element_by_css_selector(
                    'body > div.gt_holder.gt_popup.gt_show > div.gt_popup_wrap > div.gt_popup_box > div.gt_slider > div.gt_slider_knob.gt_show'):
                
                self.driver.delete_all_cookies()
                self.driver.refresh()
                Login.login(self,False)
        except:

            print('something wrong with start move')
            pass