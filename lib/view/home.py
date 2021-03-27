import cv2, PySimpleGUI as sg
from view import user, training, recognition, importData

def screenHome():
    # sg.theme('DarkTeal12')
    # ! TOOLBAR MENU
    toolbar_menu = [
        ['File', ['User', 'Operator', 'Images', 'Training','Import Data', 'Exit']],
        ['Recognition', ['Eigenfaces', 'Fisherface', 'LBPH']]
    ]
    # ! LAYOUT
    layout = [
        [sg.Menu(toolbar_menu)],
        [sg.Image(r'background/bg.png')]
    ]
    window = sg.Window('Menu', layout).Finalize()
    window.Maximize()

    while True:
        event, value = window.read()
        
        # * Screen main
        if event == 'User':
            user.screenUser()
        if event == 'Training':
            training.recognitionTraining()
        if event == 'Import Data':
            importData.importData()
        if event == 'Eigenfaces':
            recognition.eigenfaces()
        if event == 'LBPH':
            recognition.lbph()
        if event == 'Fisherface':
            recognition.fisherface()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
    window.close()