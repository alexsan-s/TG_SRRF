from controller.database.crud import *
import cv2
import numpy as np

def captura():
    classificador = cv2.CascadeClassifier(
        "haarcascade/haarcascade_frontalface_default.xml")
    classificadorOlho = cv2.CascadeClassifier("haarcascade/haarcascade_eye.xml")

    camera = cv2.VideoCapture(0)
    amostra = 1
    numeroAmostra = 20
    # nome    = input('Digite seu nome: ')
    # tel     = input('Digite seu telefone: ')
    # createUser(nome, tel)
    # id = readUser(nome)
    

    largura, altura = 220, 220

    while (True):
        conectado, imagem = camera.read()
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        print(np.average(imagemCinza))  
        facesDetectadas = classificador.detectMultiScale(
            imagemCinza, scaleFactor=1.5, minSize=(150, 150))

        for(x, y, l, a,) in facesDetectadas:
            cv2.rectangle(imagem, (x, y), (x+l, y+a), (0, 0, 255), 2)
            # regiao = imagem[y:y+a, x:x + l]
            # regiaoCinzaOlho = cv2.cvtColor(regiao, cv2.COLOR_BGR2GRAY)
            # olhosDetectaqdos = classificadorOlho.detectMultiScale(regiaoCinzaOlho)
            # for(ox, oy, ol, oa) in olhosDetectaqdos:
            #     cv2.rectangle(regiao, (ox, oy), (ox+ol, oy+oa), (0, 255, 0), 2)

                # if(cv2.waitKey(1) & 0xFF == ord('q')):
                #     if(np.average(imagemCinza) > 110):
                #         imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
                #         cv2.imwrite("assets/pessoa."+str(id)+'.' + str(amostra)+".jpg", 
                #                     imagemFace)
                #         print("[foto " + str(amostra) + " capturada com sucesso")
                #         amostra += 1
                        

        cv2.imshow("SRRF", imagem)
        cv2.waitKey(1)
        if(amostra > numeroAmostra):
            break

    camera.release()
    cv2.destroyAllWindows()
