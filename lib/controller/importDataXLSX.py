import openpyxl
from controller.database.conf import *

def importXLSX(table, file_path):
    try:
        wb = openpyxl.load_workbook(filename=file_path)

        sheet = wb.active

        if table == 'Operator':
            importOperator(sheet)
    except:
        print('falha')


def importOperator(sheet):
    try:
        column = 9
        row = 3
        valueData = ''
        # Discover how much column has
        for x in range(1, column):
            value = sheet.cell(row=row, column= x).value
            if value == None:
                break
            if isinstance(value, int):
                valueData = valueData + str(value) + ','
            else:
                valueData = valueData + "'" + str(value) + "',"
        valueData = valueData[:-1]
        sql = 'INSERT INTO OPERATOR(NAME, TELEFONE, CPF, EMAIL, LOGIN, PASSWORD, PASS_HASH, INACTIVE) VALUES('
        sql = sql + valueData
        sql = sql + ');'
        #debug
        #print(sql) 
        

        elephant = configurationElephant()
        cur = elephant.cursor()
        cur.execute(sql)
        elephant.commit()
        elephant.close()
        print("Record inserted sucessfully")
        row = row + 1

    except:
        print('falha de import')
    