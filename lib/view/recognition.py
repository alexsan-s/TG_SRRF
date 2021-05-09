from controller.database.crud import *
import PySimpleGUI as sg
import cv2
import numpy as np


#
# * Method that will show the user that is in the camera
# TODO: Create a screen that permit show more information about the user
#
#
def eigenfaces():
    layout = [
        [sg.Image(filename='', key='image', visible=True)],
        [sg.Text(text="Nome: ", key='Name', size=(80,0))]
    ]


    detectorFace = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    reconhecedor = cv2.face.EigenFaceRecognizer_create()
    reconhecedor.read("classifier/classifierEigen.yml")
    largura, altura = 200, 200
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    camera = cv2.VideoCapture(0)
    user = readAllClient()
    dataUser = {}
    for x in user:        
        dataUser[x[0]] = x[1]

    window = sg.Window('Eigenfaces', layout)


    while(True):
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event is None:
            break
        
        conectado, imagem = camera.read()
        imageGray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        facesDetectadas = detectorFace.detectMultiScale(imageGray, scaleFactor=1.5, minSize=(30,30))

        for(x,y,l,a) in facesDetectadas:
            imageFace = cv2.resize(imageGray[y:y + a, x:x + l], (largura, altura))
            cv2.rectangle(imagem, (x,y), (x+l, y+a), (0,0,255), 1)
            id, conhecedor = reconhecedor.predict(imageFace)
            print(id)
            if id in dataUser:
                window.Element('Name').update(value=dataUser[id])
                cv2.putText(imagem, dataUser[id], (x,y+(a+30)),font, 2, (0,0,255))

        window.FindElement('image').Update(data=cv2.imencode('.png', imagem)[1].tobytes())

    camera.release()
    cv2.destroyAllWindows()
    window.close()

#
# * Method that will show the user that is in the camera
# TODO: Create a screen that permit show more information about the user
#
#
def fisherface():
    layout = [
        [sg.Image(filename='', key='image', visible=True)],
        [sg.Text(text="Nome: ", key='Name', size=(80,0))]
    ]

    detectorFace = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    reconhecedor = cv2.face.EigenFaceRecognizer_create()
    reconhecedor.read("classifier/classifierFisher.yml")
    largura, altura = 200, 200
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    camera = cv2.VideoCapture(0)
    user = readAllClient()
    dataUser = {}
    for x in user:
        print(x[0])
        print(x[1])
        
        dataUser[x[0]] = x[1]
    window = sg.Window('Fisherface', layout)


    while(True):
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event is None:
            break
        conectado, imagem = camera.read()
        imageGray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        facesDetectadas = detectorFace.detectMultiScale(imageGray, scaleFactor=1.5, minSize=(30,30))

        for(x,y,l,a) in facesDetectadas:
            imageFace = cv2.resize(imageGray[y:y + a, x:x + l], (largura, altura))
            cv2.rectangle(imagem, (x,y), (x+l, y+a), (0,0,255), 1)
            id, conhecedor = reconhecedor.predict(imageFace)
            print(id)
            if id in dataUser:
                window.Element('Name').update(value=dataUser[id])
                cv2.putText(imagem, dataUser[id], (x,y+(a+30)),font, 2, (0,0,255))

        window.FindElement('image').Update(data=cv2.imencode('.png', imagem)[1].tobytes())

    camera.release()
    cv2.destroyAllWindows()
    window.close()

#
# * Method that will show the user that is in the camera
# TODO: Create a screen that permit show more information about the user
#
#
def lbph():
    clientRecog = {}
    layout = [
        [sg.Image(filename='', key='image', visible=True)],
        [sg.Text(text="Nome: ", key='Name', size=(80,0))]
    ]

    detectorFace = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    reconhecedor = cv2.face.LBPHFaceRecognizer_create()
    reconhecedor.read("classifier/classifierLBPH.yml")
    largura, altura = 200, 200
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    camera = cv2.VideoCapture(0)
    user = readAllClient()
    i = 0
    dataUser = {}
    for x in user:        
        dataUser[x[0]] = x[1]

    window = sg.Window('LBPH', layout)


    while(True):
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event is None:
            break
        conectado, imagem = camera.read()
        imageGray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        facesDetectadas = detectorFace.detectMultiScale(imageGray, scaleFactor=1.5, minSize=(30,30))

        for(x,y,l,a) in facesDetectadas:
            # print(np.average(imageGray))
            if(np.average(imageGray) > 60):
                imageFace = cv2.resize(imageGray[y:y + a, x:x + l], (largura, altura))
                cv2.rectangle(imagem, (x,y), (x+l, y+a), (0,0,255), 1)
                id, conhecedor = reconhecedor.predict(imageFace)
                # print(id)
                if id in dataUser:
                    try:
                        window.Element('Name').update(value=dataUser[id])
                        cv2.putText(imagem, dataUser[id], (x,y+(a+30)),font, 2, (0,0,255))
                        if id in clientRecog:
                            temp = clientRecog[id]
                            clientRecog[id] = temp + 1
                        else:
                            clientRecog[id] = 1
                        # print(clientRecog[id])
                        if clientRecog[id] > 30:
                            print(id)
                            i = id
                    except:
                        print('falhando')
        if i != 0:
            idProduct = readPurchasesPromotionByPKClient(i)
            nameProduct = []
            for row in idProduct:
                nameProduct.append(readProductByPk(row[0]))
            if nameProduct:
                msg = ""
                for row in nameProduct:
                    msg = msg + '{}\n'.format(row[0][1])
                sg.ScrolledTextBox('{}\n'.format(msg))
            break 
        window.FindElement('image').Update(data=cv2.imencode('.png', imagem)[1].tobytes())

    camera.release()
    cv2.destroyAllWindows()
    window.close()