import numpy
import time
import cv2
from tkinter import *
import tkinter.messagebox
root = Tk()
root.geometry('950x548')
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH, expand=1)
root.title('PPS - SRF')
frame.config(background='white')
# label = Label(frame, text="PPS - SRF",bg='white',font=('Times 35 bold'))
# label.pack(side=TOP)
filename = PhotoImage(file="assets/background/bg.png")
background_label = Label(frame, image=filename)
background_label.pack(side=TOP)

menu = Menu(root)
root.config(menu=menu)


def Contri():
    tkinter.messagebox.showinfo("Contribuidores", "\nAlexsander da Silva")


def anotherWin():
    tkinter.messagebox.showinfo(
        "Sobre", 'SRRF versão v1.0\n Uitilizando\n-OpenCV\n-Numpy\n-Tkinter\n Em Python 3')

subm1 = Menu(menu)
menu.add_cascade(label="Camera", menu=subm1)
# subm1.add_command(label="Abrir a camera", command=web)

subm3 = Menu(menu)
menu.add_cascade(label="Sobre", menu=subm3)
subm3.add_command(label="SRRF", command=anotherWin)
subm3.add_command(label="Aluno", command=Contri)

root.mainloop()
