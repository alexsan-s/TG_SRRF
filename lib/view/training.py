import PySimpleGUI as sg
import os
import cv2
import numpy as np




def getImageId():
    ways = [os.path.join('assets', f) for f in os.listdir('assets')]
    faces = []
    ids = []

    for imageWay in ways:
        imageFace = cv2.cvtColor(cv2.imread(imageWay), cv2.COLOR_BGR2GRAY)
        id = int(os.path.split(imageWay)[-1].split('.')[0])
        ids.append(id)
        faces.append(imageFace)
    return np.array(ids), faces

#
# * Screen that will do the training for the recognition
# ! Will create tree archive yml
#
def recognitionTraining():
    eigenface   = cv2.face.EigenFaceRecognizer_create()
    fisherface  = cv2.face.FisherFaceRecognizer_create()
    lbph        = cv2.face.LBPHFaceRecognizer_create()

    # layout
    layout = [
    [sg.Text("Treinamento de Reconhecimento Facial", justification='Center', size=(None,1))],
    [sg.Button(button_text="Treinar"), sg.Exit(button_text="Cancelar")],
    [sg.ProgressBar(3, orientation='h', size=(20, 20), key='progressbar', visible=False)], 
    ]
    window = sg.Window('Treinamento', layout)

    while True:
        event, values = window.Read(timeout=20, timeout_key='timeout')
        if event is None or event == 'Cancelar':  
            break
        if event == 'Treinar':
            window.Element('Treinar').Update(disabled = True)
            ids, faces = getImageId()
            window.Element('progressbar').update(0, visible=True)
            eigenface.train(faces, ids)
            eigenface.write('classifierEigen.yml')
            window.FindElement('progressbar').UpdateBar(1)  
            fisherface.train(faces, ids)
            fisherface.write('classifierFisher.yml')
            window.FindElement('progressbar').UpdateBar(2)  
            lbph.train(faces, ids)
            lbph.write('classifierLBPH.yml')
            window.FindElement('progressbar').UpdateBar(3)  
            sg.Popup('Treinamento realizado com sucesso')
            break
    window.close()