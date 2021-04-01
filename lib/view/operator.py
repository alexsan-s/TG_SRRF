import cv2, PySimpleGUI as sg
from controller.database.crud import *
import numpy as np
import os

#
# * Function that going to see the screen of client
#
#
def operatorNewOld(pk_operator = None):
    if pk_operator != None:
        data = readOperatorByPk(pk_operator)
        name = data[0][1]
        telefone = data[0][2]
        cpf = data[0][3]
        email = data[0][4]
        login = data[0][5]
        password = data[0][6]
        btnInsertUpdate = 'Update'
        title = 'Edit Operator {}'.format(name)
    else:
        name = ''
        telefone = ''
        cpf = ''
        email = ''
        login = ''
        password = ''
        btnInsertUpdate = 'Register'
        title = 'New Operator'

    # ! LAYOUT
    layout = [
        [sg.Text("Name", size=(10,1), key='lblName'), sg.Input(name, key = 'IName')],
        [sg.Text("Telefone", size=(10,1)), sg.Input(telefone, key = 'ITelefone')], 
        [sg.Text("CPF", size=(10,1)), sg.Input(cpf, key = 'ICPF')],
        [sg.Text("Email", size=(10,1), key='lblEmail'), sg.Input(email, key = 'IEmail')],
        [sg.Text("Login", size=(10,1), key='lblLogin'), sg.Input(login, key = 'ILogin')],
        [sg.Text("Password", size=(10,1), key='lblPassword'), sg.Input(password, key = 'IPassword', password_char='*')],
        [sg.HorizontalSeparator()],
        [sg.Button(button_text=btnInsertUpdate), sg.Exit(button_text="Cancel")],
        [sg.Image(filename='', key='image', visible=False)],
        [sg.ProgressBar(20, orientation='h', size=(20, 20), key='progressbar', visible=False), sg.Text('Fotos capturadas: 0', key='txtCapture', size=(20,1), visible=False)], 
        [sg.Button(button_text="Capture", visible=False)],    
    
    ]
    window = sg.Window(title, layout)


    while True:
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event is None or event == 'Cancel':  
            break
        
        if event == 'Register':
            if createClient(values) == 1:
                window.close()
                capture(2)
            else:
                sg.Popup('Fail in register')
        if event == 'Update':
            updateClient(values, pk_operator)
    window.close()

#
# * Screen that going to capture new images for have more people images selected
#
#
def capture(selected_row):
    pictures        = []
    camera          = cv2.VideoCapture(0)
    ways            = [os.path.join('assets', f) for f in os.listdir('assets')]
    classificador   = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
    
    layout = [
        [sg.Image(filename='', key='image', visible=True)],
        [sg.Button(button_text='Capture', key='btnCapture'), sg.Button(button_text='Exit', key='btnExit')],
    ]
    window = sg.Window('New Images', layout)
    
    # ! Take the last number the client picture
    for imageWay in ways:
        id = int(os.path.split(imageWay)[-1].split('.')[0])
        if id == selected_row:
            pictures.append(int(os.path.split(imageWay)[-1].split('.')[1]))
    pictures = sorted(pictures, key=int)
    try:
        lastPicture = pictures[-1] + 1
    except:
        lastPicture = 1
    
    #

    while True:
        event, value = window.read(timeout=20)
        if event == sg.WIN_CLOSED or event == 'btnExit':
            break

        ret, image = camera.read()
        imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        facesDetectadas = classificador.detectMultiScale(imageGray, scaleFactor=1.5, minSize=(150, 150))
        if ret:
            for(x, y, l, a,) in facesDetectadas:
                if(np.average(imageGray) > 110):
                    cv2.rectangle(image, (x, y), (x+l, y+a), (0, 0, 255), 2)
                    imageFace = cv2.resize(imageGray[y:y + a, x:x + l], (200, 200))
                    if event == 'btnCapture':
                        cv2.imwrite("./assets/{}.{}.jpg".format(str(selected_row),str(lastPicture)), imageFace)
                        lastPicture = lastPicture + 1
                        sg.Popup('Capture of face has registered successfully')
        window.FindElement('image').Update(data=cv2.imencode('.png', image)[1].tobytes())  
    window.close()


#
# *     Function that going to use to see the screen of Operator
# TODO: Create the function that if right clicked show an options for to do
# TODO: Update the screen when delete an Operator or when create a new Operator
#
def screenOperator():

    # ! toolbar
    toolbar_menu = [
        ['File', ['New', 'Edit', 'Delete', 'Exit']],
    ]
    data = readAllOperator()
    header = ['Code','Name', 'Email', 'Login']
    
    # ! layout
    if not data:
        dataRegister = [
            [sg.Text(text='No register')]
        ]
    else:
        dataRegister = [
            [sg.Table(values=data, headings=header, num_rows=18, row_height=20, max_col_width=100, justification='left', key='tbOperator', enable_events=True)]
        ]

    layout = [
        [sg.Menu(toolbar_menu)],
        [sg.Column(dataRegister)],
        [sg.Frame(title='Filter', layout=[
            [sg.InputCombo(['Name', 'Telefone','CPF','email','login'], key='cbmFilter', default_value = 'Name'), sg.Input('', key='lblInput')],
            [sg.Button(button_text='Search'), sg.Button(button_text='Clear')]
        ])]
    ]
    window = sg.Window('Operator', layout,size=(800,500))

    while True:
        event, value = window.read(timeout=20)
        
        if event == 'New':
            operatorNewOld()
            data = readAllOperator()
            window.Element('tbOperator').update(values=data)
        if event == 'Edit':
            operatorNewOld(window.Element('tbOperator').Values[window.Element('tbOperator').SelectedRows[0]][0])
            data = readAllOperator()
            window.Element('tbOperator').update(values=data)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        if event == 'Delete':
            if deleteClient(window.Element('tbOperator').Values[window.Element('tbOperator').SelectedRows[0]][0]) == 1:
                data = readAllOperator()
                window.Element('tbOperator').update(values=data)
        if event == 'Search':
                data = readClientFilter(value['cbmFilter'], value['lblInput'])
                window.Element('tbOperator').update(values=data)
        if event == 'Clear':
            data = readAllOperator()
            window.Element('tbOperator').update(values=data)
    window.close()

