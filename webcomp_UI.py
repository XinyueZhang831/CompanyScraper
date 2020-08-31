import PySimpleGUI as sg
from Company_scrapy_git import *
from threading import Thread

def startit():
    if len(glob.glob(os.getcwd()+'/'+'setting_info.txt')) >0:
        values =json.load(open("setting_info.txt"))
    else:
        values = {'0':False, '1':False, '2':'0', '3':False, '4':'smtp.xxxxx.com', '5':'xinyue', '6':'xinyue@xxxxx.com', '7':'ABCDEFGH', '8':'Server need to reset', '9':'Adsl name', '10':'Adsl password'}
    GUI_build(values)

def GUI_build(value):

    form = sg.FlexForm('TXX Scraping')  # begin with a blank form
    layout = [
        [sg.Text('Give input parameters: ')],
        [sg.Checkbox('First time run?')],
        [sg.Checkbox('Manually decide start number?')],
        [sg.Text('Comapany number: ', size=(15, 1)), sg.InputText(value['2'])],
        [sg.Text('Give only if want to change the number manualy', size=(30, 2))],
        [sg.Checkbox('Send notification from your email?')],
        [sg.Text('If yes, give your authoration code and email address')],
        [sg.Text('Mail host: ', size=(15, 1)), sg.InputText(value['4'])],
        [sg.Text('Mail user: ', size=(15, 1)), sg.InputText(value['5'])],
        [sg.Text('Emaill address: ', size=(15, 1)), sg.InputText(value['6'])],
        [sg.Text('Authoration code: ', size=(15, 1)), sg.InputText(value['7'])],
        [sg.Text('Send content: ', size=(15, 1)), sg.InputText(value['8'])],
        [sg.Text('Adsl name: ', size=(15, 1)), sg.InputText(value['9'])],
        [sg.Text('Adsl password: ', size=(15, 1)), sg.InputText(value['10'])],
        [sg.Ok()]
    ]

    button, values = form.Layout(layout).Read()

    overall = [values[0], values[1], values[2],values[3], [values[4], values[5], values[6], values[7], values[8]], values[9],values[10]]

    json.dump(values, open("setting_info.txt", 'w'))
    print(overall)
    start_scraping(overall)


def emailme():
    cmd = 'python'+ os.getcwd()+'/Emailme.py'
    subprocess.run(cmd,shell=True)

def scrapying():
    cmd = 'python '+ os.getcwd()+'/Company_scrapy_git.py'
    subprocess.run(cmd,shell=True)


def start_scraping(values):
    first_run = values[0]
    manual_num = values[1]
    comp_num = values[2]
    noti_check = values[3]

    parent_dir = os.getcwd() + '/'
    directory = ['1','2','3','4','5','6']

    if first_run:
        try:
            for i in directory:
                save_path = os.path.join(parent_dir, i)
                os.mkdir(save_path)
        except:
            pass
        CompNum(num=comp_num).create_file()

    if manual_num:
        CompNum(num = comp_num).overwrite_file()

    if noti_check:
        Thread(target=emailme).start()

    Thread(target=scrapying).start()
    print('yes')



if __name__ == "__main__":
    # execute only if run as a script
    startit()
