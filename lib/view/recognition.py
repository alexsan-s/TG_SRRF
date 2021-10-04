from cv2 import Algorithm, data
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
    clientRecog = {}
    msgLog = ""
    
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
    clientRecog = {}
    msgLog = ""

    layout = [
        [
            sg.Image(filename='', key='image', visible=True, size=(200,200)), 
            sg.Multiline(default_text=msgLog, size=(50, 20), key='txtLog', autoscroll=True, disabled = True)
        ],
    ]

    detectorFace = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    reconhecedor = cv2.face.FisherFaceRecognizer_create()
    reconhecedor.read("classifier/classifierFisher.yml")
    largura, altura = 200, 200
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    camera = cv2.VideoCapture(0)
    user = readAllClient()
    i = 0
    dataUser = {}
    for x in user:
        dataUser[x[0]] = x[1]

    window = sg.Window('Fisherface', layout)
    
    count = 0
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
            if(np.average(imageGray) > 60):
                if id in dataUser:
                    try:
                        cv2.putText(imagem, dataUser[id], (x,y+(a+30)),font, 2, (0,0,255))
                        if id in clientRecog:
                            temp = clientRecog[id]
                            clientRecog[id] = temp + 1
                        else:
                            clientRecog[id] = 1
                        if clientRecog[id] > 30:
                            i = id
                    except:
                        print('falhando')
        if i != 0:
            idProduct = readPurchasesPromotionByPKClient(i)
            nameProduct = []
            for row in idProduct:
                nameProduct.append(readProductByPk(row[0]))
            if nameProduct:
                msg = dataUser[i] + ' - '
                for row in nameProduct:
                    msg = msg + '{}; '.format(row[0][1])
            clientRecog[id] = 0

            msgLog = msgLog + msg + '\n'
            dataUser.pop(i)
            i=0
            window.Element('txtLog').update(value=msgLog)
        window.FindElement('image').Update(data=cv2.imencode('.png', imagem)[1].tobytes())

    camera.release()
    cv2.destroyAllWindows()
    window.close()

#
# * Method that will show the user that is in the camera
#
#
def lbph():
    clientRecog = {}
    msgLog = ""

    layout = [
        [
            sg.Image(filename='', key='image', visible=True, size=(200,200)), 
            sg.Multiline(default_text=msgLog, size=(50, 20), key='txtLog', autoscroll=True, disabled = True)
        ],
    ]

    detectorFace = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    reconhecedor = cv2.face.LBPHFaceRecognizer_create()
    reconhecedor.read("classifier/classifierLBPH.yml")
    largura, altura = 200, 200
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    camera = cv2.VideoCapture(0)
    i = 0
    dataUser = {}
    user = readAllClient()
    for x in user:        
        dataUser[x[0]] = x[1]
    print(dataUser)
    window = sg.Window('LBPH', layout)

    count = 0
    while(True):
        count = count + 1
        print(count)
        if count > 100:
            dataUser = {}
            user = readAllClient()
            for x in user:        
                dataUser[x[0]] = x[1]
            count = 0
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event is None:
            break
        conectado, imagem = camera.read()
        imageGray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        facesDetectadas = detectorFace.detectMultiScale(imageGray, scaleFactor=1.5, minSize=(30,30))

        for(x,y,l,a) in facesDetectadas:
            if(np.average(imageGray) > 60):
                imageFace = cv2.resize(imageGray[y:y + a, x:x + l], (largura, altura))
                cv2.rectangle(imagem, (x,y), (x+l, y+a), (0,0,255), 1)
                id, loss = reconhecedor.predict(imageFace)
                if loss < 50:
                    if id in dataUser:
                        try:
                            cv2.putText(imagem, dataUser[id], (x,y+(a+30)),font, 2, (0,0,255))
                            if id in clientRecog:
                                temp = clientRecog[id]
                                clientRecog[id] = temp + 1
                            else:
                                clientRecog[id] = 1
                            if clientRecog[id] > 30:
                                i = id
                        except:
                            print('falhando')
        if i != 0:
            idProduct = readPurchasesPromotionByPKClient(i)
            nameProduct = []
            for row in idProduct:
                nameProduct.append(readProductByPk(row[0]))
            if nameProduct:
                msg = dataUser[i] + ' - '
                for row in nameProduct:
                    msg = msg + '{}; '.format(row[0][1])
            clientRecog[id] = 0

            msgLog = msgLog + msg + '\n'
            dataUser.pop(i)
            i=0
            window.Element('txtLog').update(value=msgLog)
        window.FindElement('image').Update(data=cv2.imencode('.png', imagem)[1].tobytes())

    camera.release()
    cv2.destroyAllWindows()
    window.close()

def test():
    import glob
    from view import graph

    msgLog = ""
    dataUser = {}
    largura, altura = 200, 200

    user = readAllClient()
    for x in user:        
        dataUser[x[0]] = x[1]

    layout = [
        [
            [sg.Text('Chose the file'), sg.InputText(key='txtImage'), sg.FolderBrowse(), sg.Submit(button_text='Submit', key ='btnSubmit')],
            sg.Multiline(default_text=msgLog, size=(80, 20), key='txtLog', autoscroll=True, disabled = True)
        ],
    ]

    detectorFace = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

    window = sg.Window('Algorithm test', layout)

    count = 0
    while(True):
        count = count + 1
        if count > 100:
            dataUser = {}
            user = readAllClient()
            for x in user:        
                dataUser[x[0]] = x[1]
            count = 0

        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event is None:
            break
        if event == "btnSubmit":

            algorithm = {
                'Algorithms': ['Eigen', 'Fisher', 'LBPH'],
                'Found': [0,0,0],
                'Total': [0,0,0]
                # 'Eigen': [0,0],
                # 'Fisher': [0,0],
                # 'LBPH': [0,0]
            }

            # algorithmEigen = {'found': 0, 'total': 0}
            # algorithmFisher = {'found': 0, 'total': 0}
            # algorithmLBPH = {'found': 0, 'total': 0}
            
            reconhecedorEigen = cv2.face.EigenFaceRecognizer_create()
            reconhecedorEigen.read("classifier/classifierEigen.yml")
            for filename in glob.glob(values['txtImage'] + '/*.jpg'):
                imagem = cv2.imread(filename)
                imageGray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
                facesDetectadas = detectorFace.detectMultiScale(imageGray, scaleFactor = 1.11, minNeighbors=7, minSize = (30, 30))
                countFaces = 0
                for(x, y, l, a) in facesDetectadas:
                    if(np.average(imageGray) > 60):
                        imageFace = cv2.resize(imageGray[y:y + a, x:x + l], (largura, altura))
                        cv2.rectangle(imagem, (x,y), (x+l, y+a), (0,0,255), 1)

                        id, loss = reconhecedorEigen.predict(imageFace)
                        print("EigenFace: " + str(loss))
                        if loss < 500:
                            if id in dataUser:
                                countFaces = countFaces + 1
                                algorithm['Found'][0] =  algorithm['Found'][0] + 1
                if countFaces == 0 :
                    countFaces = 1
                algorithm['Total'][0] = algorithm['Total'][0] + countFaces
            
            reconhecedorFisher = cv2.face.FisherFaceRecognizer_create()
            reconhecedorFisher.read("classifier/classifierFisher.yml")
            for filename in glob.glob(values['txtImage'] + '/*.jpg'):
                imagem = cv2.imread(filename)
                imageGray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
                facesDetectadas = detectorFace.detectMultiScale(imageGray, scaleFactor = 1.11, minNeighbors=7, minSize = (30, 30))
                countFaces = 0
                for(x, y, l, a) in facesDetectadas:
                    if(np.average(imageGray) > 60):
                        imageFace = cv2.resize(imageGray[y:y + a, x:x + l], (largura, altura))
                        cv2.rectangle(imagem, (x,y), (x+l, y+a), (0,0,255), 1)
                        id, loss = reconhecedorFisher.predict(imageFace)

                        print("FisherFace: " + str(loss))
                        if loss < 100:
                            if id in dataUser:
                                countFaces = countFaces + 1
                                algorithm['Found'][1] =  algorithm['Found'][1] + 1
                if countFaces == 0 :
                    countFaces = 1
                algorithm['Total'][1] = algorithm['Total'][1] + countFaces
            
            reconhecedorLBPH = cv2.face.LBPHFaceRecognizer_create()
            reconhecedorLBPH.read("classifier/classifierLBPH.yml")
            for filename in glob.glob(values['txtImage'] + '/*.jpg'):
                imagem = cv2.imread(filename)
                imageGray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
                facesDetectadas = detectorFace.detectMultiScale(imageGray, scaleFactor = 1.11, minNeighbors=7, minSize = (30, 30))
                countFaces = 0
                for(x, y, l, a) in facesDetectadas:
                    if(np.average(imageGray) > 60):
                        imageFace = cv2.resize(imageGray[y:y + a, x:x + l], (largura, altura))
                        cv2.rectangle(imagem, (x,y), (x+l, y+a), (0,0,255), 1)

                        id, loss = reconhecedorLBPH.predict(imageFace)
                        print("LBPH: " + str(loss))
                        if loss < 50:
                            if id in dataUser:
                                countFaces = countFaces + 1
                                algorithm['Found'][2] =  algorithm['Found'][2] + 1
                if countFaces == 0 :
                    countFaces = 1
                algorithm['Total'][2] = algorithm['Total'][2] + countFaces
            msgLog = 'The EigenFaces algorithm recognized {} faces in total of {} \n '.format(algorithm['Found'][0], algorithm['Total'][0]) + '\n'
            msgLog = msgLog + 'The FisherFace algorithm recognized {} faces in total of {} \n '.format(algorithm['Found'][1], algorithm['Total'][1]) + '\n'
            msgLog = msgLog + 'The LBPG algorithm recognized {} faces in total of {} \n '.format(algorithm['Found'][2], algorithm['Total'][2]) + '\n'
            window.Element('txtLog').update(value=msgLog)
            graph.plotGraphAlgorithms(algorithm)
    cv2.destroyAllWindows()
    window.close()