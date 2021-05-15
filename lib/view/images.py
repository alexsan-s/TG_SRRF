import cv2, PySimpleGUI as sg
from controller.database.crud import *

#
# *     Function that going to use to see the screen of CLIENT
# TODO: Create the function that if right clicked show an options for to do
# TODO: Update the screen when delete an client or when create a new client
#
def screen():

    data = readPicture()
    header = ['Picture']

    # ! toolbar
    toolbar_menu = [
        ['File', ['Exit']],
    ]

    # First the window layout in 2 columns
    file_list_column = [
        [
            sg.Listbox(
                values=data, enable_events=True, size=(60, 30), key="lbData"
            )
        ],
    ]

    # For now will only show the name of the file that was chosen
    image_viewer_column = [
        [sg.Text("Choose an image from list on left:")],
        [sg.Image(key="image")],
    ]

    # ----- Full layout -----
    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(image_viewer_column),
        ]
    ]
    window = sg.Window('Images', layout,size=(800,500))

    while True:
            event, value = window.read(timeout=20)
            
            if event == 'Exit' or event == sg.WIN_CLOSED:
                break
            if value['lbData']:
                img = cv2.imread('assets/{}'.format(value['lbData'][0][0]), 0) 
                try:
                    window.FindElement('image').Update(data=cv2.imencode('.png', img)[1].tobytes())
                except:
                    del img
                    sg.Popup("Can't found the image")
    window.close()

