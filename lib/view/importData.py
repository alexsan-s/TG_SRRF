import cv2, PySimpleGUI as sg
from view import user, training, recognition
from controller import importDataXLSX

def importData():
    # ! LAYOUT
    layout = [
        [sg.Text("Choose what do you want to import"), sg.InputCombo(['Operator', 'Controller'], key='Combo')],
        [sg.Text('Chose the file'), sg.InputText(key='TXT_PATH'), sg.FileBrowse()],
        [sg.Button(button_text='Import')],
    ]
    window = sg.Window('Import', layout).Finalize()
    window.Maximize()

    while True:
        event, value = window.read()

        if event == 'Import':
            msg = importDataXLSX.importXLSX(value['Combo'], value['TXT_PATH'])
            sg.Print(msg)

        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
    window.close()