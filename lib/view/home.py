import cv2, PySimpleGUI as sg
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

    while True:
        event, value = window.read()
        
        # * Screen main
        if event == "Logout":   
            from view import login         
            yesNo = sg.popup_yes_no("Are you sure?", title='Logout',)
            if yesNo == "Yes":
                window.close()
                login.login()
        if event == 'Client':
            from view import client
            client.screenClient()
        if event == 'Operator':
            from view import operator
            operator.screenOperator()
        if event == 'Product':
            from view import product
            product.screen()
        if event == 'Images':
            from view import images
            images.screen()
        if event == 'Training':
            from view import training
            training.recognitionTraining()
        if event == 'Import Data':
            from view import importData
            importData.importData()
        if event == 'Eigenfaces':
            from view import recognition
            recognition.eigenfaces()
        if event == 'Fisherface':
            from view import recognition
            recognition.fisherface()
        if event == 'LBPH':
            from view import recognition
            recognition.lbph()
        if event == 'Buy':
            from view import buy
            buy.screenBuy()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
    window.close()