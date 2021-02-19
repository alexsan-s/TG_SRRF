from controller import captura, reconhecedorEigefaces


opUSer = True

print("----------------------------")
print("         BEM VINDO          ")
print("----------------------------")
while opUSer:
    print("O que deseja?")
    print("1) Cadastrar")
    print("2) Reconhecimento facial Eigenfaces")
    print("0) Sair")
    option = input("Digitar: ")
    
    if(option == '1'):
        captura.captura()
    if(option == '2'):
        reconhecedorEigefaces.recognizerEigenface()
    if(option == '0'):
        opUSer = False

