import cv2, PySimpleGUI as sg
from controller.database.crud import *
import numpy as np
import os

#
# * Function that going to see the screen of new user
#
#
def newUser():
    # ! VARIABLES
    id = 0
    count = 0
    created = False
    camera = None
    classificador = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")

    # ! LAYOUT
    layout = [
        [sg.Text("Name", size=(10,1)), sg.Input('', key = 'IName')],
        [sg.Text("Telefone", size=(10,1)), sg.Input('', key = 'ITelefone')],
        [sg.Text("CPF", size=(10,1)), sg.Input('', key = 'ICPF')],
        [sg.Button(button_text="Register"), sg.Exit(button_text="Cancel")],
        [sg.Image(filename='', key='image', visible=False)],
        [sg.ProgressBar(20, orientation='h', size=(20, 20), key='progressbar', visible=False), sg.Text('Fotos capturadas: 0', key='txtCapture', size=(20,1), visible=False)], 
        [sg.Button(button_text="Capture", visible=False)],
        
    ]
    window = sg.Window('New User', layout, size=(952,516))


    while True:
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event is None or event == 'Cancel':  
            break
        if event == 'Register':
            if createUser(values['IName'], values['ITelefone'], values['ICPF']) == 1:
                id = readUser(values['ICPF'])
                window.Element('IName').Update(disabled=True)
                window.Element('ITelefone').Update(disabled=True)
                window.Element('image').Update(visible=True)
                window.Element('progressbar').update(0, visible=True)
                window.FindElement('txtCapture').update(visible = True)
                window.Element('Capture').Update(visible=True)
                created = True
                camera  = cv2.VideoCapture(0)
            else:
                sg.Popup('Fail in register')

        if created:
            if count == 20:
                window.close()
                sg.Popup('Capture of face has registered successfully')
                break

            ret, imagem = camera.read()
            imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            facesDetectadas = classificador.detectMultiScale(
                imagemCinza, scaleFactor=1.5, minSize=(150, 150))
            if ret:
                for(x, y, l, a,) in facesDetectadas:
                    cv2.rectangle(imagem, (x, y), (x+l, y+a), (0, 0, 255), 2)
                    if(np.average(imagemCinza) > 110):
                        imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (200, 200))
                        if event == 'Capture':
                            count = count + 1
                            cv2.imwrite("{}.{}.jpg".format(str(id),str(count)), imagemFace)
                            window.FindElement('txtCaptura').update(value = 'Pictures captured: {}'.format(count))
                            window.FindElement('progressbar').UpdateBar(count)            
            window.FindElement('image').Update(data=cv2.imencode('.png', imagem)[1].tobytes())  
    if(created):      
        camera.release()
    window.close()

#
# * Screen that going to capture new images for have more people images selected
#
#
def capture(selected_row):
    camera  = cv2.VideoCapture(0)
    ways = [os.path.join('assets', f) for f in os.listdir('assets')]
    ids = []
    
    layout = [
        [sg.Image(filename='', key='image', visible=True)],
        [sg.Button(button_text='Capture', key='btnCapture')],
    ]
    window = sg.Window('New Images', layout)

    for imageWay in ways:
        id = int(os.path.split(imageWay)[-1].split('.')[1])
        ids.append(id)
    print(faces)
    while True:
        event, value = window.read(timeout=20)
        if(event == sg.WIN_CLOSED):
            break
        if(event == 'btnCapture'):
            print(selected_row)

        ret, imagem = camera.read()
        window.FindElement('image').Update(data=cv2.imencode('.png', imagem)[1].tobytes())  
    window.close()


#
# *     Function that going to use to see the screen of User
# TODO: Create the function that if right clicked show an options for to do
# TODO: Update the screen when delete an user or when create a new user
#
def screenUser():

    # ! toolbar
    toolbar_menu = [
        ['File', ['New', 'Delete', 'Exit']],
        ['Insert', ['Capture']],
    ]
    data = readAllUser()
    header = ['Code','Name', 'Telefone', 'CPF']
    
    # ! layout
    col_layout = [
        [sg.Table(values=data, headings=header, auto_size_columns=True, justification='left', key='tbUser', enable_events=True)]
    ]
    layout = [
        [sg.Menu(toolbar_menu)],
        [sg.Column(col_layout)]
    ]
    window = sg.Window('User', layout)

    while True:
        event, value = window.read(timeout=20)
        
        if event == 'New':
            newUser()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        if event == 'Delete':
            deleteUser(selected_row)
        if event == 'Capture':
            capture(selected_row)
        if event == 'tbUser':
            selected_row = data[value[event][0]][0]
            print(selected_row)
    window.close()

