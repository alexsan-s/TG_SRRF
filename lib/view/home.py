import cv2, PySimpleGUI as sg
from view import client, operator, training, recognition, importData
from controller.toolbar import toolbarMenu

def screenHome():
    # sg.theme('DarkTeal12')
    # ! TOOLBAR MENU
    toolbar_menu = toolbarMenu('home')
    # ! LAYOUT
    layout = [
        [sg.Menu(toolbar_menu)],
    ]
    window = sg.Window('Menu', layout, size=(800,500)).Finalize()
    window.Maximize()

    while True:
        event, value = window.read()
        
        # * Screen main
        if event == 'Client':
            client.screenClient()
        if event == 'Operator':
            operator.screenOperator()
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