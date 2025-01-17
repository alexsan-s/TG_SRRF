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
        data        = readClientByPk(pk_client)
        name        = data[0][1]
        cpf         = data[0][2]
        if data[0][3] == 'null': 
            rg      = ''    
        else: 
            rg      = data[0][3]
        birth       = data[0][4]
        sex         = data[0][5]
        if sex == 'M':
            sexM    = True
            sexF    = False
            sexI    = False
        elif sex == 'F':
            sexM    = False
            sexF    = True
            sexI    = False
        else:
            sexM    = False
            sexF    = False
            sexI    = True
        email       = data[0][6]
        if data[0][7]   == 'null': 
            cep     = '' 
        else:
            cep     = data[0][7]     
        if data[0][8]   == 'null': 
            address = '' 
        else:
            address = data[0][8]     
        if data[0][9]   == 'null': 
            number  = '' 
        else:
            number  = data[0][9]     
        if data[0][10]  == 'null': 
            district= '' 
        else:
            district= data[0][10]    
        if data[0][11]  == 'null': 
            city    = '' 
        else:
            city    = data[0][11]    
        if data[0][12]  == 'null': 
            state   = '' 
        else:
            state   = data[0][12]    
        if data[0][13]  == 'null': 
            telefone= '' 
        else:
            telefone= data[0][13]    
        cell        = data[0][14]
        btnInsertUpdate = 'Update'
        title       = 'Edit client {}'.format(name)
    else:
        name        = ''
        cpf         = ''
        rg          = ''
        birth       = ''
        sexM        = False
        sexF        = False
        sexI        = True
        email       = ''
        cep         = ''
        address     = ''
        number      = ''
        district    = ''
        city        = ''
        state       = ''
        telefone    = ''
        cell        = ''
        btnInsertUpdate = 'Register'
        title       = 'New client'

    # ! LAYOUT
    layout = [
        [sg.Text("Name", size=(10,1), key='lblName'), sg.Input(name, key = 'IName')],
        [sg.Text('',size=(20,1), key='lblErrorName', visible=False)],
        [sg.Text("CPF", size=(10,1)), sg.Input(cpf, key = 'ICpf')],
        [sg.Text("RG", size=(10,1)), sg.Input(rg, key = 'IRg')],
        [sg.Text("Birth", size=(10,1)), sg.Input(birth, key= 'IBirth'),sg.CalendarButton("Pick date", format='%Y-%m-%d')],
        [sg.Text("Sex", size=(10,1)), sg.Radio("Masc", "RADIO1", key='R1', default=sexM), sg.Radio("Fem", "RADIO1", key='R2', default=sexF), sg.Radio("Undefined", "RADIO1", key='R3', default=sexI)],
        [sg.Text("Email", size=(10,1), key='lblEmail'), sg.Input(email, key = 'IEmail')],
        [sg.Frame(layout=[
            [sg.Text("Cep", size=(10,1)), sg.Input(cep, key = 'ICep')],
            [sg.Text("Address", size=(10,1)), sg.Input(address, key = 'IAddress')],
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
        [sg.Button(button_text="Capture", visible=False)],    
    
    ]
    window = sg.Window(title, layout)


    while True:
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event is None or event == 'Cancel':  
            break
        
        if event == 'Register':
            register = createClient(values)
            if register == 1:
                window.close()
                pk_client = readClientByCpf(values['ICpf'])
                capture(pk_client[0][0], newUser=True)
            elif register == 0:
                sg.Popup('Fail in register')
            elif register == -1:
                sg.Popup('Invalid name')
            elif register == -2:
                sg.Popup('Invalid cpf')
            elif register == -3:
                sg.Popup('Invalid rg')
            elif register == -4:
                sg.Popup('Invalid birth')
            elif register == -5:
                sg.Popup('Invalid sex')
            elif register == -6:
                sg.Popup('Invalid email')
            elif register == -7:
                sg.Popup('Invalid cep')
            elif register == -8:
                sg.Popup('Invalid address')
            elif register == -9:
                sg.Popup('Invalid number')
            elif register == -10:
                sg.Popup('Invalid district')
            elif register == -11:
                sg.Popup('Invalid city')
            elif register == -12:
                sg.Popup('Invalid state')
            elif register == -13:
                sg.Popup('Invalid telefone')
            elif register == -14:
                sg.Popup('Invalid cell')
        if event == 'Update':
            updated = updateClient(values, pk_client)   
            if updated == 1:
                sg.Popup('Updated successfully')
            elif updated == 0:
                sg.Popup('Fail in updated')
            elif updated == -1:
                sg.Popup('Invalid name')
            elif updated == -2:
                sg.Popup('Invalid cpf')
            elif updated == -3:
                sg.Popup('Invalid rg')
            elif updated == -4:
                sg.Popup('Invalid birth')
            elif updated == -5:
                sg.Popup('Invalid sex')
            elif updated == -6:
                sg.Popup('Invalid email')
            elif updated == -7:
                sg.Popup('Invalid cep')
            elif updated == -8:
                sg.Popup('Invalid address')
            elif updated == -9:
                sg.Popup('Invalid number')
            elif updated == -10:
                sg.Popup('Invalid district')
            elif updated == -11:
                sg.Popup('Invalid city')
            elif updated == -12:
                sg.Popup('Invalid state')
            elif updated == -13:
                sg.Popup('Invalid telefone')
            elif updated == -14:
                sg.Popup('Invalid cell') 

    window.close()

#
# * Screen that going to capture new images for have more people images selected
#
#
def capture(pk_client, newUser = False):
    pictures        = []
    count           = 0
    camera          = cv2.VideoCapture(0)
    ways            = [os.path.join('assets', f) for f in os.listdir('assets')]
    classificador   = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
    
    layout = [
        [sg.Text('Chose the file'), sg.InputText(key='txtImage'), sg.FileBrowse(), sg.Submit(button_text='Submit', key ='btnSubmit')],
        [sg.Image(filename='', key='image', visible=True)],
        [sg.Button(button_text='Capture', key='btnCapture'), sg.Button(button_text='Exit', key='btnExit')],
        [sg.ProgressBar(20, orientation='h', size=(20, 20), key='progressbar', visible=newUser), sg.Text('Fotos capturadas: 0', key='txtCapture', size=(20,1), visible=newUser)], 
    ]
    window = sg.Window('New Images', layout)
    
    # ! Take the last number the client picture
    if not newUser:
        try:
            lastPicture = readClientPicture(pk_client)[0][0]
        except:
            lastPicture = 1
    #Debug
    # print(lastPicture)

    # for imageWay in ways:
    #     id = int(os.path.split(imageWay)[-1].split('.')[0])
    #     if id == pk_client:
    #         pictures.append(int(os.path.split(imageWay)[-1].split('.')[1]))
    # pictures = sorted(pictures, key=int)
    # try:
    #     lastPicture = pictures[-1] + 1
    # except:
    #     lastPicture = 1
    
    #

    while True:
        event, value = window.read(timeout=20)
        if event == sg.WIN_CLOSED or event == 'btnExit':
            break

        if newUser:
            if count == 20:
                window.close()
                sg.Popup('Capture of face has registered successfully')
                break
        if event == 'btnSubmit':
            try:
                path = value['txtImage']
                image = cv2.imread(path)
                imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                facesDetectadas = classificador.detectMultiScale(imageGray, scaleFactor = 1.11, minNeighbors=7, minSize = (30, 30))
                for(x, y, l, a) in facesDetectadas:
                    cv2.rectangle(image, (x, y), (x + l, y+a), (0, 0, 255), 2)
                    imageFace = cv2.resize(imageGray[y:y + a, x:x + l], (200, 200))
                    if newUser:
                        count = count + 1
                        if insertPicture(pk_client, count) == 1:
                            cv2.imwrite("./assets/{}.{}.jpg".format(str(pk_client),str(count)), imageFace)
                            window.FindElement('txtCapture').update(value = 'Pictures captured: {}'.format(count))
                    else:
                        if insertPicture(pk_client, lastPicture) == 1:
                            cv2.imwrite("./assets/{}.{}.jpg".format(str(pk_client),str(lastPicture)), imageFace)
                            lastPicture = lastPicture + 1
                            sg.Popup('Capture of face has registered successfully')
                        else:
                            sg.Popup('Fail to registerred in the database.')
            except:
                sg.Popup('Fail to read the image.')

        ret, image = camera.read()
        imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        facesDetectadas = classificador.detectMultiScale(imageGray, scaleFactor=1.5, minSize=(150, 150))
        if ret:
            for(x, y, l, a,) in facesDetectadas:
                # if(np.average(imageGray) > 110):
                    cv2.rectangle(image, (x, y), (x+l, y+a), (0, 0, 255), 2)
                    imageFace = cv2.resize(imageGray[y:y + a, x:x + l], (200, 200))
                    if event == 'btnCapture':
                        if newUser:
                            count = count + 1
                            if insertPicture(pk_client, count) == 1:
                                cv2.imwrite("./assets/{}.{}.jpg".format(str(pk_client),str(count)), imageFace)
                                window.FindElement('txtCapture').update(value = 'Pictures captured: {}'.format(count))
                                window.FindElement('progressbar').UpdateBar(count) 
                            else:
                                sg.Popup('Fail to registerred in the database.')
                        else:
                            if insertPicture(pk_client, lastPicture) == 1:
                                cv2.imwrite("./assets/{}.{}.jpg".format(str(pk_client),str(lastPicture)), imageFace)
                                lastPicture = lastPicture + 1
                                sg.Popup('Capture of face has registered successfully')
                            else:
                                sg.Popup('Fail to registerred in the database.')
        window.FindElement('image').Update(data=cv2.imencode('.png', image)[1].tobytes())  
    camera.release()
    window.close()

def purchases(pk_client):
    purchases_date = readPurchases(pk_client)
    listDate = []
    listProduct = []
    for row in purchases_date:
        listDate.append(row[0])

    header = ['Code','Product', 'Qtd']
    data = []
    toolbar_menu = [
            ['File', ['Exit']],
        ]
    layout = [
        [sg.Menu(toolbar_menu)],
        [
            sg.Column(
                [
                    [sg.Listbox(values = listDate, size=(30,100), key='lbList', enable_events=True)]
                ]
            ),
            sg.Column(
                [
                    [sg.Table(values=data, headings=header, num_rows=18, row_height=20, max_col_width=40, justification='left', key='tbProduct', enable_events=True,auto_size_columns=False, col_widths=[10, 30, 10])]
                ]
            )
        ],
    ]


    window = sg.Window('Client', layout,size=(800,500))

    while True:
        event, value = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        if event == 'lbList':
            print(value['lbList'])
            listProduct = readPurchases(pk_client, value['lbList'])
            window.Element('tbProduct').Update(values = listProduct)

        
    window.close()
#
# *     Function that going to use to see the screen of CLIENT
# TODO: Create the function that if right clicked show an options for to do
#
def screenClient(find = False):

    # ! toolbar
    if not find:
        toolbar_menu = [
            ['File', ['New', 'Edit', 'Delete', 'Exit']],
            ['Insert', ['Capture']],
            ['View', ['Purchases']],
        ]
    else:
        toolbar_menu = [
            ['File', ['Exit']],
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
            [sg.Table(values=data, headings=header, num_rows=18, row_height=20, max_col_width=40, justification='left', key='tbClient', enable_events=True, auto_size_columns=False, col_widths=[5, 40, 35])],
        ]
        if find:
            dataRegister.append([sg.Submit()])

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
        try:
            event, value = window.read(timeout=20)
            
            if event == 'Exit' or event == sg.WIN_CLOSED:   
                break
            if event == 'New':
                clientNewOld()
                data = readAllClient()
                window.Element('tbClient').update(values=data)
            if event == 'Edit':
                clientNewOld(window.Element('tbClient').Values[window.Element('tbClient').SelectedRows[0]][0])
                data = readAllClient()
                window.Element('tbClient').update(values=data)
            if event == 'Delete':
                if deleteClient(window.Element('tbClient').Values[window.Element('tbClient').SelectedRows[0]][0]) == 1:
                    data = readAllClient()
                    window.Element('tbClient').update(values=data)
            if event == 'Capture':
                capture(window.Element('tbClient').Values[window.Element('tbClient').SelectedRows[0]][0])
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
            if event == 'Submit':
                pk_client = window.Element('tbClient').Values[window.Element('tbClient').SelectedRows[0]]
                break
            if event == 'Purchases':
                purchases(window.Element('tbClient').Values[window.Element('tbClient').SelectedRows[0]][0])
        except IndexError:
            sg.Popup("Select a client")
    window.close()
    if find:
        try:
            return pk_client
        except UnboundLocalError:
            return None

