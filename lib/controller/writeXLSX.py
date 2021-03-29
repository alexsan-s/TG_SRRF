from openpyxl import Workbook
from tkinter import *
import tkinter.filedialog

def writeXLSX(typeXLSX):    
    sourcePath = filedialog.askdirectory()

    wb = Workbook()
    ws = wb.active

    if typeXLSX == 'Operator':
        ws['A1'] = 'NAME'
        ws['B1'] = 'TELEFONE'
        ws['C1'] = 'CPF'
        ws['D1'] = 'EMAIL'
        ws['E1'] = 'LOGIN'
        ws['F1'] = 'PASSWORD'
        ws['G1'] = 'INACTIVE'
        fileName = '{}/ImportOperator.xlsx'.format(sourcePath)
    if typeXLSX == 'Product':
        ws['A1'] = 'PRODUCT'
        ws['B1'] = 'DESCRIPTION'
        ws['C1'] = 'INACTIVE'
        fileName = '{}/ImportProduct.xlsx'.format(sourcePath)
    if typeXLSX == 'Client':
        ws['A1'] = 'NAME'
        ws['B1'] = 'EMAIL'
        ws['C1'] = 'TELEFONE'
        ws['D1'] = 'CPF'
        fileName = '{}/ImportClient.xlsx'.format(sourcePath)

    wb.save(fileName)
