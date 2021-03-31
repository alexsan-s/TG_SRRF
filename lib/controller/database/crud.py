from controller.database.conf import *
import psycopg2

# ! CREATE TABLES

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
        sql = """INSERT INTO CLIENT(NAME, CPF, RG, BIRTH, SEX, EMAIL, CEP, ADDRESS, NUMBER, DISTRICT, CITY, STATE, TELEFONE, CELL) VALUES('{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}');""".format(values['IName'],values['ICPF'],values['IRG'],values['IDate'],IRadio,values['IEmail'], values['ICep'],values['IAdrress'],values['INumber'],values['IDistrict'],values['ICity'],values['IState'],values['ITelefone'],values['ICell'])
        cur.execute(sql)
        conf.commit()
        conf.close()
        print("Record inserted sucessfully")
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

# ! READ TABLES

def readClientByPk(pk_cliente):
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT * FROM CLIENT WHERE PK_CLIENT = {};".format(pk_cliente)
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

def readUser(cpf):
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT ID FROM CLIENT WHERE CPF = '" + cpf + "';"
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows[0][0]

def readAllClient():
    conf = configurationElephant()
    cur = conf.cursor()
    sql = "SELECT PK_CLIENT, NAME, EMAIL FROM CLIENT;"
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
