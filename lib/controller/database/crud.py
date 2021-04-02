from controller.database.conf import *
from controller import function
import psycopg2
import hashlib

# ! INSERT TABLES

def createClient(values):
    try:
        name        = 'null'
        cpf         = 'null'
        rg          = 'null'
        birth       = 'null'
        sex         = 'null'
        email       = 'null'
        cep         = 'null'
        address     = 'null'
        number      = 'null'
        district    = 'null'
        city        = 'null'
        state       = 'null'
        telefone    = 'null'
        cell        = 'null'
        # 1
        name = function.capitalizeWord(values['IName'])
        if len(name) <= 3:
            return -1

        #2
        cpf = function.validadeCPF(values['ICpf'])
        if cpf:
            cpf = values['ICpf']
            if readClientByCpf(cpf):
                return -2
        else:
            return -2

        #3
        if len(values['IRg']) >= 1:
            rg = function.validadeRg(values['IRg'])
            if rg:
                rg = values['IRg']
                if readClientByRg(cpf):
                    return -2
            else:
                return -3

        #4
        birth = function.validadeDate(values['IBirth'])
        if birth:
            birth = values['IBirth']
        else:
            return -4
        
        #5
        if values['R1'] == True:
            sex = "M"
        elif values['R2'] == True:
            sex = "F" 
        else: 
            sex = "I"

        #6
        email = function.validadeEmail(values['IEmail'])
        if email:
            email = function.capitalizeWord(values['IEmail'])
        else:
            return -6

        #7
        if len(values['ICep']) >= 1:
            cep = function.validadeCep(values['ICep'])
            if cep:
                cep = function.capitalizeWord(values['ICep'])
            else:
                return -7
        
        #8
        if len(values['IAddress']) >= 1:
            address = function.capitalizeWord(values['IAddress'])

        #9
        if len(values['INumber']) >= 1:
            number = function.validadeNumber(values['INumber'])
            if number:
                number = values['INumber']
            else:
                return -9

        #10
        if len(values['IDistrict']) >= 1:
            district = function.capitalizeWord(values['IDistrict'])

        #11
        if len(values['ICity']) >= 1:
            city = function.capitalizeWord(values['ICity'])

        #12
        if len(values['IState']) >= 1:
            if len(values['IState']) == 2:
                state = function.capitalizeWord(values['IState'])
            else:
                return -12

        #13
        if len(values['ITelefone']) >= 1:
            telefone = function.validadeTelefone(values['ITelefone'])
            if telefone:
                telefone = values['ITelefone']
            else:
                return -13

        #14
        cell = function.validadeTelefone(values['ICell'])
        if cell:
            cell = values['ICell']
        else:
            return -14
        
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "INSERT INTO CLIENT(NAME, CPF, RG, BIRTH, SEX, EMAIL, CEP, ADDRESS, NUMBER, DISTRICT, CITY, STATE, TELEFONE, CELL) VALUES('{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}');".format(name, cpf, rg, birth, sex, email, cep, address, number, district, city, state, telefone, cell)
        cur.execute(sql)
        conf.commit()
        conf.close()
        print("Record inserted sucessfully")
        return 1
    except:
        return 0

def createOperator(values):
    try:
        # 1
        name = function.capitalizeWord(values['IName'])
        if len(name) <= 3:
            return -1
        
        #2 
        telefone = function.validadeTelefone(values['ITelefone'])
        if telefone:
            telefone = values['ITelefone']
        else:
            return -2

        #3
        cpf = function.validadeTelefone(values['ICpf'])
        if cpf:
            cpf = values['ICpf']
        else:
            return -3

        #4
        email = function.validadeEmail(values['IEmail'])
        if email:
            email = function.capitalizeWord(values['IEmail'])
        else:
            return -4

        #5
        login = function.capitalizeWord(values['ILogin'])
        if len(login) <= 3:
            return -5
        
        #6
        password = function.validadePassword(values['IPassword'])
        if password:
            password = values['IPassword']
            pass_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()
        else:
            return -6

            

        conf = configurationElephant()
        cur = conf.cursor()
        sql = "INSERT INTO OPERATOR(NAME, TELEFONE, CPF, EMAIL, LOGIN, PASSWORD, PASS_HASH, INACTIVE) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', {})".format(name, telefone, cpf, email, login, password, pass_hash, 0)
        #Debug
        # print(sql)
        cur.execute(sql)
        conf.commit()
        conf.close()
        return 1
    except:
        return 0

def insertPicture(pk_client, picture):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "INSERT INTO CLIENT_PICTURE(PK_CLIENT, PICTURE) VALUES({}, '{}')".format(pk_client, picture)
        #Debug
        print(sql)

        cur.execute(sql)
        conf.commit()
        conf.close()
        return 1
    except:
        return 0
# ! UPDATE TABLES

def updateClient(values, pk_client):
    try:
        name        = 'null'
        cpf         = 'null'
        rg          = 'null'
        birth       = 'null'
        sex         = 'null'
        email       = 'null'
        cep         = 'null'
        address     = 'null'
        number      = 'null'
        district    = 'null'
        city        = 'null'
        state       = 'null'
        telefone    = 'null'
        cell        = 'null'
        # 1
        name = function.capitalizeWord(values['IName'])
        if len(name) <= 3:
            return -1

        #2
        cpf = function.validadeCPF(values['ICpf'])
        if cpf:
            cpf = values['ICpf']
            if readClientByCpf(cpf, pk_client = pk_client):
                return -2
        else:
            return -2

        #3
        if len(values['IRg']) >= 1:
            rg = function.validadeRg(values['IRg'])
            if rg:
                rg = values['IRg']
                if readClientByRg(cpf):
                    return -2
            else:
                return -3

        #4
        birth = function.validadeDate(values['IBirth'])
        if birth:
            birth = values['IBirth']
        else:
            return -4
        
        #5
        if values['R1'] == True:
            sex = "M"
        elif values['R2'] == True:
            sex = "F" 
        else: 
            sex = "I"

        #6
        email = function.validadeEmail(values['IEmail'])
        if email:
            email = function.capitalizeWord(values['IEmail'])
        else:
            return -6

        #7
        if len(values['ICep']) >= 1:
            cep = function.validadeCep(values['ICep'])
            if cep:
                cep = function.capitalizeWord(values['ICep'])
            else:
                return -7
        
        #8
        if len(values['IAddress']) >= 1:
            address = function.capitalizeWord(values['IAddress'])

        #9
        if len(values['INumber']) >= 1:
            number = function.validadeNumber(values['INumber'])
            if number:
                number = values['INumber']
            else:
                return -9

        #10
        if len(values['IDistrict']) >= 1:
            district = function.capitalizeWord(values['IDistrict'])

        #11
        if len(values['ICity']) >= 1:
            city = function.capitalizeWord(values['ICity'])

        #12
        if len(values['IState']) >= 1:
            if len(values['IState']) == 2:
                state = function.capitalizeWord(values['IState'])
            else:
                return -12

        #13
        if len(values['ITelefone']) >= 1:
            telefone = function.validadeTelefone(values['ITelefone'])
            if telefone:
                telefone = values['ITelefone']
            else:
                return -13

        #14
        cell = function.validadeTelefone(values['ICell'])
        if cell:
            cell = values['ICell']
        else:
            return -14

        conf = configurationElephant()
        cur = conf.cursor()
        sql = "UPDATE CLIENT SET NAME = '{}', CPF = '{}', RG = '{}', BIRTH = '{}', SEX = '{}', EMAIL = '{}', CEP = '{}', ADDRESS = '{}', NUMBER = '{}', DISTRICT = '{}', CITY = '{}', STATE = '{}', TELEFONE = '{}', CELL = '{}' WHERE PK_CLIENT = {}".format(name, cpf, rg, birth, sex, email, cep, address, number, district, city, state, telefone, cell, pk_client)
        cur.execute(sql)
        conf.commit()
        conf.close()
        print("Record update sucessfully")
        return 1
    except:
        return 0

def updateOperator(values, pk_operator):
    try:
        # 1
        name = function.capitalizeWord(values['IName'])
        if len(name) <= 3:
            return -1
        
        #2 
        telefone = function.validadeTelefone(values['ITelefone'])
        if telefone:
            telefone = values['ITelefone']
        else:
            return -2

        #3
        cpf = function.validadeTelefone(values['ICpf'])
        if cpf:
            cpf = values['ICpf']
        else:
            return -3

        #4
        email = function.validadeEmail(values['IEmail'])
        if email:
            email = function.capitalizeWord(values['IEmail'])
        else:
            return -4

        #5
        login = function.capitalizeWord(values['ILogin'])
        if len(login) <= 3:
            return -5
        
        #6
        password = function.validadePassword(values['IPassword'])
        if password:
            password = values['IPassword']
            pass_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()
        else:
            return -6

        #7
        inactive = values['IInactive']
        if inactive:
            inactive = 1
        else:
            inactive = 0

        conf = configurationElephant()
        cur = conf.cursor()
        pass_hash = hashlib.sha1(values['IPassword'].encode('utf-8')).hexdigest()
        sql = "UPDATE OPERATOR SET NAME = '{}', TELEFONE = '{}', CPF = '{}', EMAIL = '{}', LOGIN = '{}', PASSWORD = '{}', PASS_HASH = '{}', INACTIVE = '{}' WHERE PK_OPERATOR = {}".format(name, telefone, cpf, email, login, password, pass_hash, inactive, pk_operator)
        #Debug
        # print(sql)
        cur.execute(sql)
        conf.commit()
        conf.close()
        return 1
    except:
        return 0
# ! READ TABLES

def readClientByPk(pk_client):
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT * FROM CLIENT WHERE PK_CLIENT = {};".format(pk_client)
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

def readOperatorByPk(pk_operator):
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT * FROM OPERATOR WHERE PK_OPERATOR = {};".format(pk_operator)
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

def readClientPicture(pk_client):
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT COUNT(PICTURE) + 1 FROM CLIENT_PICTURE WHERE pk_client = '{}';".format(pk_client)
    #Bebug
    # print(sql)
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

def readClientByCpf(cpf, pk_client = None):
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT PK_CLIENT FROM CLIENT WHERE CPF = '{}'".format(cpf)
    if pk_client:
        sql += 'AND PK_CLIENT <> {}'.format(pk_client)
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

def readClientByRg(rg):
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT PK_CLIENT FROM CLIENT WHERE RG = '" + rg + "';"
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

def readClientFilter(table, filter):
    table = function.capitalizeWord(table)
    filter = function.capitalizeWord(filter)
    conf = configurationElephant()
    cur = conf.cursor()
    if table == 'Birth':
        sql = "SELECT PK_CLIENT, NAME, EMAIL FROM CLIENT WHERE {} = '{}' ORDER BY NAME;".format(table, filter)
    elif table == 'Number':
        sql = "SELECT PK_CLIENT, NAME, EMAIL FROM CLIENT WHERE {} = {} ORDER BY NAME;".format(table, filter)
    else:
        sql = "SELECT PK_CLIENT, NAME, EMAIL FROM CLIENT WHERE {} LIKE '%{}%' ORDER BY NAME;".format(table, filter)
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

def readOperatorFilter(table, filter):
    table = function.capitalizeWord(table)
    filter = function.capitalizeWord(filter)
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT PK_OPERATOR, NAME, EMAIL, LOGIN FROM OPERATOR WHERE {} LIKE '%{}%' ORDER BY NAME;".format(table, filter)
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

def readAllClient():
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT PK_CLIENT, NAME, EMAIL FROM CLIENT ORDER BY PK_CLIENT ORDER BY NAME;"
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

def readAllOperator():
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT PK_OPERATOR, NAME, EMAIL, LOGIN FROM OPERATOR ORDER BY PK_OPERATOR ORDER BY NAME;"
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

def readLogin(login, password):
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT PK_OPERATOR FROM OPERATOR WHERE LOGIN = '{}' AND PASS_HASH = '{}' AND INACTIVE = 0;".format(login, password)
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

def readPicture():
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT CONCAT(PK_CLIENT,'.',PICTURE,'.jpg') FROM CLIENT_PICTURE ORDER BY PK_CLIENT_PICTURE"
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows
# ! DROP TABLE
def deleteClient(cod):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "DELETE FROM CLIENT WHERE PK_CLIENT = '{}';".format(cod)
        cur.execute(sql)
        conf.commit()
        conf.close()
        return 1
    except:
        return 0

def deleteOperator(cod):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "DELETE FROM OPERATOR WHERE PK_OPERATOR = '{}';".format(cod)
        cur.execute(sql)
        conf.commit()
        conf.close()
        return 1
    except:
        return 0