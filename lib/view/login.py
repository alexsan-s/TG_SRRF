import PySimpleGUI as sg
import hashlib
from controller.database.crud import *
from view import home

#
# * Screen that going to permit if the user has login
#
def login():
    # ! LAYOUT
    layout = [
        [sg.Text(text="Login:", size=(10,1)), sg.Input(key='ILogin')],
        [sg.Text(text="Password:", size=(10,1)), sg.Input(key='IPassword', password_char='*')],
        [sg.Button(button_text='Login'), sg.Button(button_text='Cancel')],
        [sg.Text(text="", visible=False, key="lblMsg", size=(30,0))]
    ]
    window = sg.Window('Login', layout)

    while True:
        event, value = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Login':
            res = searchLogin(value)
            if res == 0:
                window.Element('lblMsg').Update(value='Fail to access', visible=True)
            else:
                window.close()
                home.screenHome()
        
#
# * Validate login
#
def searchLogin(value):
    try:
        pass_hash = hashlib.sha1(value['IPassword'].encode('utf-8')).hexdigest()
        row = readLogin(value['ILogin'], pass_hash)
        if not row:
            return 0
        else:
            return 1
    except:
        return 0


