import openpyxl
import hashlib
from datetime import datetime
from controller.database.conf import *

def importXLSX(table, file_path):
    try:
        wb = openpyxl.load_workbook(filename=file_path)

        sheet = wb.active

        if table == 'Operator':
            return importOperator(sheet)
        if table == 'Product':
            return importProduct(sheet)
    except:
        return 'Fail to read the file XLSX'


def importOperator(sheet):
    try:
        column = 9
        row = 2
        valueData = ''
        msg = ''

        conf = configurationElephant()
        cur = conf.cursor()

        # Pass for all columns
        for y in range(row, 1000):
            error = 0

            # 1
            name = sheet.cell(row=y, column= 1).value
            if name == None:
                break
            
            # 2
            telefone    = sheet.cell(row=y, column = 2).value

            # 3
            cpf         = sheet.cell(row=y, column = 3).value
            if cpf == None:
                msg += 'Erro linha {}: O campo CPF[{}] não está preenchido.\n'.format(str(y), cpf)
                error += 1
            else:
                sql = "SELECT CPF FROM OPERATOR WHERE CPF = '{}'".format(cpf)
                cur.execute(sql)
                rows = cur.fetchall()
                if rows:
                    msg += 'Erro linha {}: O CPF[{}] já existe no banco de dados e não pode ser inserido.\n'.format(str(y), cpf)
                    error += 1
            # 4
            if error == 0:
                email       = sheet.cell(row=y, column = 4).value
                if email == None:
                    msg += 'Erro linha {}: O campo email[{}] não está preenchido.\n'.format(str(y), email)
                    error += 1
                else:
                    sql = "SELECT EMAIL FROM OPERATOR WHERE EMAIL = '{}'".format(email)
                    cur.execute(sql)
                    rows = cur.fetchall()
                    if rows:
                        msg += 'Erro linha {}: O EMAIL[{}] já existe no banco de dados e não pode ser inserido.\n'.format(str(y), email)
                        error += 1
            # 5
            if error == 0:
                login       = sheet.cell(row=y, column = 5).value
                if login == None:
                    msg += 'Erro linha {}: O campo login[{}] não está preenchido.\n'.format(str(y), login)
                    error += 1
                else:
                    sql = "SELECT LOGIN FROM OPERATOR WHERE LOGIN = '{}'".format(login)
                    cur.execute(sql)
                    rows = cur.fetchall()
                    if rows:
                        msg += 'Erro linha {}: O LOGIN[{}] já existe no banco de dados e não pode ser inserido.\n'.format(str(y), login)
                        error += 1

            # 6
            if error == 0:
                password    = sheet.cell(row=y, column = 6).value
                if password == None:
                    password = 'Ch@nge123'
                pass_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()

                # 7
                inactive    = sheet.cell(row=y, column = 8).value
                if inactive == None:
                    inactive = 0

            if error == 0:
                sql = "INSERT INTO OPERATOR(NAME, TELEFONE, CPF, EMAIL, LOGIN, PASSWORD, PASS_HASH, INACTIVE) VALUES('{}', {}, {}, '{}', '{}', '{}', '{}', {})".format(name, telefone, cpf, email, login, password, pass_hash, inactive)
                #debug
                # print(sql) 
                try:
                    cur.execute(sql)
                    conf.commit()
                    msg += 'Ok linha {}: O Operador[{}] foi cadastrado com sucesso.\n'.format(str(y), name)
                except:
                    msg += 'Erro linha {}: O Operador[{}] não foi possível ser cadastrado.\n'.format(str(y), name)
        fileName = "ImportOperator_{}.txt".format(str(datetime.now()))
        file = open(fileName, "w") 
        file.write(str(msg))
        file.close
        conf.close()
        return msg
    except Exception:
        msg = 'Fail to read de file XSLX'
        return msg
    
def importProduct(sheet):
    try:
        row = 2
        msg = ''

        conf = configurationElephant()
        cur = conf.cursor()

        # Pass for all columns
        for y in range(row, 1000):
            error = 0

            # 1
            product = sheet.cell(row=y, column= 1).value
            if product
             == None:
                break
            
            # 2
            description    = sheet.cell(row=y, column = 2).value

            

            # 3
            inactive    = sheet.cell(row=y, column = 3).value
            if inactive == None:
                inactive = 0

            if error == 0:
                sql = "INSERT INTO PRODUCT(PRODUCT, DESCRIPTION, INACTIVE) VALUES('{}', '{}', {})".format(product, description, inactive)
                #debug
                # print(sql) 
                try:
                    cur.execute(sql)
                    conf.commit()
                    msg += 'Ok row {}: The product [{}] was registered sucefull.\n'.format(str(y), product)
                except:
                    msg += 'Error row {}: The product[{}] was not registered with successful.\n'.format(str(y), product)
        fileName = "ImportProduct{}.txt".format(str(datetime.now()))
        file = open(fileName, "w") 
        file.write(str(msg))
        file.close
        conf.close()
        return msg
    except Exception:
        msg = 'Fail to read de file XSLX'
        return msg