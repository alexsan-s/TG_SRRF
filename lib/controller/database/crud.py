from controller.database.conf import *
import psycopg2
import hashlib

# ! INSERT TABLES

def createClient(values):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        if values['R1'] == True:
            IRadio = "M"
        elif values['R2'] == True:
            IRadio = "F" 
        else: 
            IRadio = "I"
        hasCpf = readClientByCpf(values["ICPF"])
        if hasCpf:
            return 0
        sql = """INSERT INTO CLIENT(NAME, CPF, RG, BIRTH, SEX, EMAIL, CEP, ADDRESS, NUMBER, DISTRICT, CITY, STATE, TELEFONE, CELL) VALUES('{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}');""".format(values['IName'],values['ICPF'],values['IRG'],values['IDate'],IRadio,values['IEmail'], values['ICep'],values['IAdrress'],values['INumber'],values['IDistrict'],values['ICity'],values['IState'],values['ITelefone'],values['ICell'])
        cur.execute(sql)
        conf.commit()
        conf.close()
        print("Record inserted sucessfully")
        return 1
    except:
        return 0

def createOperator(values):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        pass_hash = hashlib.sha1(values['IPassword'].encode('utf-8')).hexdigest()
        sql = "INSERT INTO OPERATOR(NAME, TELEFONE, CPF, EMAIL, LOGIN, PASSWORD, PASS_HASH, INACTIVE) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', {})".format(values['IName'], values['ITelefone'], values['ICpf'], values['IEmail'], values['ILogin'], values['IPassword'], pass_hash, 0)
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
        conf = configurationElephant()
        cur = conf.cursor()
        if values['R1'] == True:
            IRadio = "M"
        elif values['R2'] == True:
            IRadio = "F" 
        else: 
            IRadio = "I"
        sql = "UPDATE CLIENT SET NAME = '{}', CPF = '{}', RG = '{}', BIRTH = '{}', SEX = '{}', EMAIL = '{}', CEP = '{}', ADDRESS = '{}', NUMBER = '{}', DISTRICT = '{}', CITY = '{}', STATE = '{}', TELEFONE = '{}', CELL = '{}' WHERE PK_CLIENT = {}".format(values['IName'],values['ICPF'],values['IRG'],values['IDate'],IRadio,values['IEmail'], values['ICep'],values['IAdrress'],values['INumber'],values['IDistrict'],values['ICity'],values['IState'],values['ITelefone'],values['ICell'], pk_client)
        cur.execute(sql)
        conf.commit()
        conf.close()
        print("Record update sucessfully")
        return 1
    except:
        return 0

def updateOperator(values, pk_operator):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        pass_hash = hashlib.sha1(values['IPassword'].encode('utf-8')).hexdigest()
        sql = "UPDATE OPERATOR SET NAME = '{}', TELEFONE = '{}', CPF = '{}', EMAIL = '{}', LOGIN = '{}', PASSWORD = '{}', PASS_HASH = '{}', INACTIVE = '{}' WHERE PK_OPERATOR = {}".format(values['IName'], values['ITelefone'], values['ICpf'], values['IEmail'], values['ILogin'], values['IPassword'], pass_hash, 0, pk_operator)
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

def readClientByCpf(cpf):
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT PK_CLIENT FROM CLIENT WHERE CPF = '" + cpf + "';"
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

def readClientFilter(table, filter):
    conf = configurationElephant()
    cur = conf.cursor()
    if table == 'Birth':
        sql = "SELECT PK_CLIENT, NAME, EMAIL FROM CLIENT WHERE {} = '{}';".format(table, filter)
    elif table == 'Number':
        sql = "SELECT PK_CLIENT, NAME, EMAIL FROM CLIENT WHERE {} = {};".format(table, filter)
    else:
        sql = "SELECT PK_CLIENT, NAME, EMAIL FROM CLIENT WHERE {} LIKE '%{}%';".format(table, filter)
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

def readOperatorFilter(table, filter):
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT PK_OPERATOR, NAME, EMAIL, LOGIN FROM OPERATOR WHERE {} LIKE '%{}%';".format(table, filter)
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

def readAllClient():
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT PK_CLIENT, NAME, EMAIL FROM CLIENT ORDER BY PK_CLIENT;"
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

def readAllOperator():
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT PK_OPERATOR, NAME, EMAIL, LOGIN FROM OPERATOR ORDER BY PK_OPERATOR;"
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