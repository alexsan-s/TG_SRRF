import cv2, PySimpleGUI as sg
from controller.database.crud import *
import numpy as np
import os

#
# * Function that going to see the screen of client
#
#
def clientNewOld(pk_client = None):
    # ! VARIABLES
    id = 0
    count = 0
    created = False
    camera = None
    classificador = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")

    if pk_client != None:
        data = readClientByPk(pk_client)
        name = data[0][1]
        cpf = data[0][2]
        rg = data[0][3]
        birth = data[0][4]
        sex = data[0][5]
        if sex == 'M':
            sexM = True
            sexF = False
            sexI = False
        elif sex == 'F':
            sexM = False
            sexF = True
            sexI = False
        else:
            sexM = False
            sexF = False
            sexI = True
        email = data[0][6]
        cep = data[0][7]
        address = data[0][8]
        number = data[0][9]
        district = data[0][10]
        city = data[0][11]
        state = data[0][12]
        telefone = data[0][13]
        cell = data[0][14]
        btnInsertUpdate = 'Update'
        title = 'Edit client {}'.format(name)
    else:
        name = ''
        cpf = ''
        rg = ''
        birth = ''
        sexM = False
        sexF = False
        sexI = True
        email = ''
        cep = ''
        address = ''
        number = ''
        district = ''
        city = ''
        state = ''
        telefone = ''
        cell = ''
        btnInsertUpdate = 'Register'
        title = 'New client'

    # ! LAYOUT
    layout = [
        [sg.Text("Name", size=(10,1), key='lblName'), sg.Input(name, key = 'IName')],
        [sg.Text('',size=(20,1), key='lblErrorName', visible=False)],
        [sg.Text("CPF", size=(10,1)), sg.Input(cpf, key = 'ICPF')],
        [sg.Text("RG", size=(10,1)), sg.Input(rg, key = 'IRG')],
        [sg.Text("Birth", size=(10,1)), sg.Input(birth, key= 'IDate'),sg.CalendarButton("Pick date", format='%Y-%m-%d')],
        [sg.Text("Sex", size=(10,1)), sg.Radio("Masc", "RADIO1", key='R1', default=sexM), sg.Radio("Fem", "RADIO1", key='R2', default=sexF), sg.Radio("Undefined", "RADIO1", key='R3', default=sexI)],
        [sg.Text("Email", size=(10,1), key='lblEmail'), sg.Input(email, key = 'IEmail')],
        [sg.Frame(layout=[
            [sg.Text("Cep", size=(10,1)), sg.Input(cep, key = 'ICep')],
            [sg.Text("Adrress", size=(10,1)), sg.Input(address, key = 'IAdrress')],
            [sg.Text("Number", size=(10,1)), sg.Input(number, key = 'INumber')],
            [sg.Text("District", size=(10,1)), sg.Input(district, key = 'IDistrict')],
            [sg.Text("City", size=(10,1)), sg.Input(city, key = 'ICity')],
            [sg.Text("State", size=(10,1)), sg.Input(state, key = 'IState')],
        ], title = "Address")],
        [sg.Frame(layout=[
            [sg.Text("Telefone", size=(10,1)), sg.Input(telefone, key = 'ITelefone')],
            [sg.Text("Cell", size=(10,1)), sg.Input(cell, key = 'ICell')],
        ], title = "Contact")],
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
            updateClient(values, pk_client)
        if created:
            if count == 20:
                window.close()
                sg.Popup('Capture of face has registered successfully')
                break

            ret, image = camera.read()
            imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            facesDetectadas = classificador.detectMultiScale(
                imageGray, scaleFactor=1.5, minSize=(150, 150))
            if ret:
                for(x, y, l, a,) in facesDetectadas:
                    cv2.rectangle(image, (x, y), (x+l, y+a), (0, 0, 255), 2)
                    if(np.average(imageGray) > 110):
                        imageFace = cv2.resize(imageGray[y:y + a, x:x + l], (200, 200))
                        if event == 'Capture':
                            count = count + 1
                            cv2.imwrite("./assets/{}.{}.jpg".format(str(id),str(count)), imageFace)
                            window.FindElement('txtCapture').update(value = 'Pictures captured: {}'.format(count))
                            window.FindElement('progressbar').UpdateBar(count)            
            window.FindElement('image').Update(data=cv2.imencode('.png', image)[1].tobytes())  
    if(created):      
        camera.release()
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
# *     Function that going to use to see the screen of CLIENT
# TODO: Create the function that if right clicked show an options for to do
# TODO: Update the screen when delete an client or when create a new client
#
def screenClient():

    # ! toolbar
    toolbar_menu = [
        ['File', ['New', 'Edit', 'Delete', 'Exit']],
        ['Insert', ['Capture']],
    ]
    data = readAllClient()
    header = ['Code','Name', 'Email']
    
    # ! layout
    if not data:
        dataRegister = [
            [sg.Text(text='No register')]
        ]
    else:
        dataRegister = [
            [sg.Table(values=data, headings=header, num_rows=18, row_height=20, max_col_width=100, justification='left', key='tbClient', enable_events=True)]
        ]

    layout = [
        [sg.Menu(toolbar_menu)],
        [sg.Column(dataRegister)],
        [sg.Frame(title='Filter', layout=[
            [sg.InputCombo(['Name', 'Cpf','Rg','Birth','Sex','Email','Cep','Address','Number','District','City','State','Telefone','Cell'], key='cbmFilter', default_value = 'Name'), sg.Input('', key='lblInput'), sg.CalendarButton("Pick date", key='btnCalendar', disabled=True, format='%Y-%m-%d')],
            [sg.Button(button_text='Search'), sg.Button(button_text='Clear')]
        ])]
    ]
    window = sg.Window('Client', layout,size=(800,500))

    while True:
        event, value = window.read(timeout=20)
        
        if event == 'New':
            clientNewOld()
            data = readAllClient()
            window.Element('tbClient').update(values=data)
        if event == 'Edit':
            clientNewOld(window.Element('tbClient').Values[window.Element('tbClient').SelectedRows[0]][0])
            data = readAllClient()
            window.Element('tbClient').update(values=data)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        if event == 'Delete':
            if deleteClient(window.Element('tbClient').Values[window.Element('tbClient').SelectedRows[0]][0]) == 1:
                data = readAllClient()
                window.Element('tbClient').update(values=data)
        if event == 'Capture':
            capture(selected_row)
        if event == 'Search':
                data = readClientFilter(value['cbmFilter'], value['lblInput'])
                window.Element('tbClient').update(values=data)
        if event == 'Clear':
            data = readAllClient()
            window.Element('tbClient').update(values=data)
        if value['cbmFilter'] == 'Birth':
            window.Element('btnCalendar').Update(disabled=False)
        else:
            window.Element('btnCalendar').Update(disabled=True)
    window.close()

