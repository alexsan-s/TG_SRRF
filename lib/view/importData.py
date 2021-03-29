import cv2, PySimpleGUI as sg
from view import user, training, recognition
from controller import importXLSX, writeXLSX

def importData():
    # ! TOOLBAR MENU
    toolbar_menu = [
        ['Models', ['Operator', 'Product', 'Client']],
    ]
    # ! LAYOUT
    layout = [
        [sg.Menu(toolbar_menu)],
        [sg.Text("Choose what do you want to import"), sg.InputCombo(['Operator', 'Product', 'Client'], key='Combo')],
        [sg.Text('Chose the file'), sg.InputText(key='TXT_PATH'), sg.FileBrowse()],
        [sg.Button(button_text='Import')],
    ]
    window = sg.Window('Import', layout).Finalize()
    window.Maximize()

    while True:
        event, value = window.read()

        if event == "Operator":
            writeXLSX.writeXLSX(event)
        if event == "Product":
            writeXLSX.writeXLSX(event)
        if event == "Client":
            writeXLSX.writeXLSX(event)

        if event == 'Import':
            msg = importXLSX.importXLSX(value['Combo'], value['TXT_PATH'])
            sg.Print(msg)

        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
    window.close()