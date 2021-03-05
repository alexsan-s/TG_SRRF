import cv2, PySimpleGUI as sg
from controller.database.crud import *
import numpy as np

#
# * Function that going to see the screen of new user
#
def newUser():
    # ! VARIABLES
    i=0
    camera = cv2.VideoCapture(0)
    classificador = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")

    # ! LAYOUT
    layout = [
        [sg.Text("Sistema de Recomendação de Reconhecimento Facial", justification='Center', size=(None,1))],
        [sg.Text("Nome", size=(10,1)), sg.Input('', key = 'INome')],
        [sg.Text("Telefone", size=(10,1)), sg.Input('', key = 'ITelefone')],
        [sg.Text("CPF", size=(10,1)), sg.Input('', key = 'ICPF')],
        [sg.Button(button_text="Cadastrar"), sg.Exit(button_text="Cancelar")],
        [sg.Image(filename='', key='image', visible=False)],
        [sg.ProgressBar(20, orientation='h', size=(20, 20), key='progressbar', visible=False), sg.Text('Fotos capturadas: 0', key='txtCaptura', size=(20,1), visible=False)], 
        [sg.Button(button_text="Capturar", visible=False)],
        
    ]
    window = sg.Window('Novo Usuário', layout)


    while True:
        event, values = window.Read(timeout=100, timeout_key='timeout')
        if event is None or event == 'Cancelar':  
            break
        if event == 'Cadastrar':
            if createUser(values['INome'], values['ITelefone']) == 1:
                window.Element('INome').Update(disabled=True)
                window.Element('ITelefone').Update(disabled=True)
                window.Element('image').Update(visible=True)
                window.Element('progressbar').update(0, visible=True)
                window.FindElement('txtCaptura').update(visible = True)
                window.Element('Capturar').Update(visible=True)
            else:
                sg.Popup('Falha em cadastrar')
        if i == 20:
            window.close()
            sg.Popup('Captura de face foi cadastrado com sucesso')
            break

        #
        # TODO: tentar utilizar o reconhecimento facial
        #
        ret, imagem = camera.read()
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        facesDetectadas = classificador.detectMultiScale(
            imagemCinza, scaleFactor=1.5, minSize=(150, 150))
        if ret:
            for(x, y, l, a,) in facesDetectadas:
                cv2.rectangle(imagem, (x, y), (x+l, y+a), (0, 0, 255), 2)
                if(np.average(imagemCinza) > 110):
                    imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (200, 200))
                    if event == 'Capturar':
                        i = i + 1
                        cv2.imwrite("assets/pessoa." + str(i)+".jpg", imagemFace)
                        window.FindElement('txtCaptura').update(value = 'Fotos capturadas: {}'.format(i))
                        window.FindElement('progressbar').UpdateBar(i)            
        window.FindElement('image').Update(data=cv2.imencode('.png', imagem)[1].tobytes())        
    camera.release()
    window.close()

#
# *     Function that going to use to see the screen of User
# TODO: Need create the option of other buttons
#
def screenUser():

    # ! toolbar
    toolbar_menu = [
        ['Arquivo', ['Novo', 'Excluir', 'Sair']],
    ]
    data = readAllUser()
    header = ['Código','Nome', 'Telefone']
    
    # ! layout
    col_layout = [
        [sg.Table(values=data, headings=header, auto_size_columns=True, justification='left', key='table', enable_events=True)]
    ]
    layout = [
        [sg.Menu(toolbar_menu)],
        [sg.Column(col_layout, size=(952,360))]
    ]
    window = sg.Window('Usuário', layout, finalize=True, location=(70,70), size=(952,516))

    while True:
        event, value = window.read(timeout=20)
        
        if event == 'Novo':
            newUser()
        if event == 'Sair' or event == sg.WIN_CLOSED:
            break
        if event == 'table':
            selected_row = data[value[event][0]]
            print(selected_row)
    window.close()

