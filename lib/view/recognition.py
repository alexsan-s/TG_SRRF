from controller.database.crud import *
import PySimpleGUI as sg
import cv2


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

    window = sg.Window('Eigenfaces', layout)


    while(True):
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event is None:
            break
        
        conectado, imagem = camera.read()
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        facesDetectadas = detectorFace.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(30,30))

        for(x,y,l,a) in facesDetectadas:
            imageFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
            cv2.rectangle(imagem, (x,y), (x+l, y+a), (0,0,255), 1)
            id, conhecedor = reconhecedor.predict(imageFace)
            if(id <= len(user)):
                window.Element('Name').update(value=user[id -1][1])
                cv2.putText(imagem, user[id-1][1], (x,y+(a+30)),font, 2, (0,0,255))

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
    window = sg.Window('Fisherface', layout)


    while(True):
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event is None:
            break
        conectado, imagem = camera.read()
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        facesDetectadas = detectorFace.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(30,30))

        for(x,y,l,a) in facesDetectadas:
            imageFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
            cv2.rectangle(imagem, (x,y), (x+l, y+a), (0,0,255), 1)
            id, conhecedor = reconhecedor.predict(imageFace)
            if(id <= len(user)):
                window.Element('Name').update(value=user[id -1][1])
                cv2.putText(imagem, user[id-1][1], (x,y+(a+30)),font, 2, (0,0,255))

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
    window = sg.Window('LBPH', layout)


    while(True):
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event is None:
            break
        conectado, imagem = camera.read()
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        facesDetectadas = detectorFace.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(30,30))

        for(x,y,l,a) in facesDetectadas:
            imageFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
            cv2.rectangle(imagem, (x,y), (x+l, y+a), (0,0,255), 1)
            id, conhecedor = reconhecedor.predict(imageFace)
            if(id <= len(user)):
                window.Element('Name').update(value=user[id -1][1])
                cv2.putText(imagem, user[id-1][1], (x,y+(a+30)),font, 2, (0,0,255))

        window.FindElement('image').Update(data=cv2.imencode('.png', imagem)[1].tobytes())

    camera.release()
    cv2.destroyAllWindows()
    window.close()