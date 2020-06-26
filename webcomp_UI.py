import PySimpleGUI as sg
from Compay_scrapy import*
import os
import glob
import json

def startit():
    if len(glob.glob(os.getcwd()+'/'+'setting_info.txt')) >0:
        values =json.load(open("setting_info.txt"))



    else:
        values = {'0':'.../Driver/chromewebdriver', '1':'.../company.csv', '2':False, '3':False, '4':'0', '5':False, '6':'smtp.163.com', '7':'xinyue', '8':'xinyue@163.com', '9':'ABCDEFGH', '10':'Server need to reset', '11':'Adsl name', '12':'Adsl password'}
    GUI_build(values)

def GUI_build(value):

    form = sg.FlexForm('Tianyancha Scraping')  # begin with a blank form
    layout = [
        [sg.Text('Give input parameters: ')],
        [sg.Text('Driver directory: ', size=(15, 1)), sg.InputText(value['0'])],
        [sg.Text('CSV file directory: ', size=(15, 1)), sg.InputText(value['1'])],
        [sg.Checkbox('First time run?')],
        [sg.Checkbox('Manually decide start number?')],
        [sg.Text('Comapany number: ', size=(15, 1)), sg.InputText(value['4'])],
        [sg.Text('Give only if want to change the number manualy', size=(30, 2))],
        [sg.Checkbox('Send notify from your email?')],
        [sg.Text('If yes, give your authoration code and email address')],
        [sg.Text('Mail host: ', size=(15, 1)), sg.InputText(value['6'])],
        [sg.Text('Mail user: ', size=(15, 1)), sg.InputText(value['7'])],
        [sg.Text('Emaill address: ', size=(15, 1)), sg.InputText(value['8'])],
        [sg.Text('Authoration code: ', size=(15, 1)), sg.InputText(value['9'])],
        [sg.Text('Send content: ', size=(15, 1)), sg.InputText(value['10'])],
        [sg.Text('Adsl name: ', size=(15, 1)), sg.InputText(value['11'])],
        [sg.Text('Adsl password: ', size=(15, 1)), sg.InputText(value['12'])],
        [sg.Ok()]
    ]

    button, values = form.Layout(layout).Read()

    overall = [values[0], values[1], values[2],values[3], values[4], values[5],[values[6], values[7], values[8], values[9],values[10]]]

    json.dump(values, open("setting_info.txt", 'w'))

    start_scraping(overall)

def start_scraping(values):
    dri_dir = values[0]
    file_dir = values[1]
    first_run = values[2]
    manual_num = values[3]
    comp_num = values[4]
    noti_check = values[5]
    email_info = values[6]
    print(dri_dir, file_dir, first_run, manual_num, comp_num, noti_check, email_info)
    #Compayscrap(dri_dir, file_dir, first_run, manual_num, comp_num, noti_check, email_info).run_scrapy()


if __name__ == "__main__":
    # execute only if run as a script
    startit()