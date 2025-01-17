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
    
def createProduct(values):
    try:
        # 1
        product = function.capitalizeWord(values['IProduct'])
        if len(product) <= 3:
            return -1
        
        #2 
        description = ""
        if len(values['IDescription']) >= 3:
            description = function.capitalizeWord(values['IDescription'])
            if description:
                description = values['IDescription']
            else:
                return -2
        #3
        promotion = values['cbPromotion']
        if promotion:
            promotion = 1
        else:
            promotion = 0

        conf = configurationElephant()
        cur = conf.cursor()
        sql = "INSERT INTO PRODUCT(PRODUCT, DESCRIPTION, INACTIVE, PROMOTION) VALUES('{}', '{}', {}, {})".format(product, description, 0, promotion)
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

def insertPurchases(pk_client):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "INSERT INTO PURCHASES(PK_CLIENT) VALUES({})".format(pk_client)
        #Debug
        # print(sql)

        cur.execute(sql)
        conf.commit()
        conf.close()
        return 1
    except:
        return 0

def insertClientProduct(pk_client, product):
    try:
        from controller import globalPy
        from datetime import datetime
        pkUser = globalPy.pkUser
        date = datetime.now().date()
        time = datetime.now()
        time = str(time.hour) + ':' + str(time.minute) + ':' + str(time.second)
        conf = configurationElephant()
        cur = conf.cursor()
        for row in product:
            for row2 in range(0, row[2]):
                sql = "INSERT INTO CLIENT_PRODUCT(PK_CLIENT, PK_PRODUCT, PK_OPERATOR, DATE_BUY, TIME) VALUES({}, {}, {}, '{}', '{}')".format(pk_client, row[0], pkUser, date, time)
                #Debug
                # print(sql)

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

def updateProduct(values, pk_product):
    try:
        # 1
        product = function.capitalizeWord(values['IProduct'])
        if len(product) <= 3:
            return -1

        #2 
        if len(values['IDescription']) >= 3:
            description = function.capitalizeWord(values['IDescription'])
            if description:
                description = values['IDescription']
            else:
                return -2 
        else: 
            description = ''
        #3
        inactive = values['IInactive']
        if inactive:
            inactive = 1
        else:
            inactive = 0

        #4
        promotion = values['cbPromotion']
        if promotion:
            promotion = 1
        else:
            promotion = 0

        conf = configurationElephant()
        cur = conf.cursor()
        sql = "UPDATE PRODUCT SET PRODUCT = '{}', DESCRIPTION = '{}', INACTIVE = '{}', PROMOTION = {} WHERE PK_PRODUCT = {}".format(product, description, inactive, promotion, pk_product)
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
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "SELECT * FROM CLIENT WHERE PK_CLIENT = {};".format(pk_client)
        cur.execute(sql)
        rows = cur.fetchall()
        conf.close()
        return rows
    except Exception:
        return []

def readOperatorByPk(pk_operator):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "SELECT * FROM OPERATOR WHERE PK_OPERATOR = {};".format(pk_operator)
        cur.execute(sql)
        rows = cur.fetchall()
        conf.close()
        return rows
    except Exception:
        return []

def readProductByPk(pk_product):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "SELECT * FROM PRODUCT WHERE PK_PRODUCT = {};".format(pk_product)
        cur.execute(sql)
        rows = cur.fetchall()
        conf.close()
        return rows
    except Exception:
        return []

def readClientPicture(pk_client):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "SELECT COUNT(PICTURE) + 1 FROM CLIENT_PICTURE WHERE pk_client = '{}';".format(pk_client)
        #Bebug
        # print(sql)
        cur.execute(sql)
        rows = cur.fetchall()
        conf.close()
        return rows
    except Exception:
        return []

def readClientByCpf(cpf, pk_client = None):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "SELECT PK_CLIENT FROM CLIENT WHERE CPF = '{}'".format(cpf)
        if pk_client:
            sql += 'AND PK_CLIENT <> {}'.format(pk_client)
        cur.execute(sql)
        rows = cur.fetchall()
        conf.close()
        return rows
    except Exception:
        return []

def readClientByRg(rg):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "SELECT PK_CLIENT FROM CLIENT WHERE RG = '" + rg + "';"
        cur.execute(sql)
        rows = cur.fetchall()
        conf.close()
        return rows
    except Exception:
        return []

def readClientFilter(table, filter):
    try:
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
    except Exception:
        return []

def readOperatorFilter(table, filter):
    try:
        table = function.capitalizeWord(table)
        filter = function.capitalizeWord(filter)
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "SELECT PK_OPERATOR, NAME, EMAIL, LOGIN FROM OPERATOR WHERE {} LIKE '%{}%' ORDER BY NAME;".format(table, filter)
        cur.execute(sql)
        rows = cur.fetchall()
        conf.close()
        return rows
    except Exception:
        return []

def readProductFilter(table, filter):
    try:
        table = function.capitalizeWord(table)
        filter = function.capitalizeWord(filter)
        conf = configurationElephant()
        cur = conf.cursor()
        if table == 'CODE':
            sql = "SELECT PK_PRODUCT, PRODUCT, DESCRIPTION FROM PRODUCT WHERE PK_PRODUCT = {} ORDER BY PRODUCT;".format(filter)
        elif table == 'PROMOTION':
            sql = "SELECT PK_PRODUCT, PRODUCT, DESCRIPTION FROM PRODUCT WHERE {} = {} ORDER BY PRODUCT;".format(table, filter)
        else:
            sql = "SELECT PK_PRODUCT, PRODUCT, DESCRIPTION FROM PRODUCT WHERE {} LIKE '%{}%' ORDER BY PRODUCT;".format(table, filter)
        cur.execute(sql)
        rows = cur.fetchall()
        conf.close()
        return rows
    except Exception:
        return []

def readAllClient():
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "SELECT PK_CLIENT, NAME, EMAIL FROM CLIENT ORDER BY NAME;"
        cur.execute(sql)
        rows = cur.fetchall()
        conf.close()
        return rows
    except Exception:
        return []

def readAllProduct():
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "SELECT PK_PRODUCT, PRODUCT, DESCRIPTION FROM PRODUCT ORDER BY PRODUCT;"
        cur.execute(sql)
        rows = cur.fetchall()
        conf.close()
        return rows
    except Exception:
        return []

def readAllOperator():
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "SELECT PK_OPERATOR, NAME, EMAIL, LOGIN FROM OPERATOR ORDER BY NAME;"
        cur.execute(sql)
        rows = cur.fetchall()
        conf.close()
        return rows
    except Exception:
        return []

def readLogin(login, password):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "SELECT PK_OPERATOR FROM OPERATOR WHERE LOGIN = '{}' AND PASS_HASH = '{}' AND INACTIVE = 0;".format(login, password)
        cur.execute(sql)
        rows = cur.fetchall()
        conf.close()
        return rows
    except Exception:
        return []

def readPicture():
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "SELECT CONCAT(PK_CLIENT,'.',PICTURE,'.jpg') FROM CLIENT_PICTURE ORDER BY PK_CLIENT_PICTURE"
        cur.execute(sql)
        rows = cur.fetchall()
        conf.close()
        return rows
    except Exception:
        return []

def readPurchases(pk_client, filterDate = False):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        if filterDate:
            from datetime import datetime
            date_day = filterDate[0].strftime('%Y-%m-%d')
            sql = """SELECT
                        CLIENT_PRODUCT.PK_PRODUCT,
                        PRODUCT.PRODUCT,
                        COUNT(CLIENT_PRODUCT.PK_PRODUCT)
                    FROM 
                        CLIENT_PRODUCT
                        LEFT JOIN PRODUCT ON (CLIENT_PRODUCT.PK_PRODUCT = PRODUCT.PK_PRODUCT)
                    WHERE 
                        CLIENT_PRODUCT.PK_CLIENT = {}
                        AND
                        CLIENT_PRODUCT.DATE_BUY = '{}'
                    GROUP BY
                        CLIENT_PRODUCT.DATE_BUY,
                        CLIENT_PRODUCT.pk_product,
                        PRODUCT.PRODUCT""".format(pk_client, date_day)
        else:
            sql = """SELECT 
                        DATE_BUY
                    FROM 
                        CLIENT_PRODUCT 
                    WHERE 
                        PK_CLIENT = {}
                    GROUP BY DATE_BUY""".format(pk_client)
        cur.execute(sql)
        rows = cur.fetchall()
        conf.close()
        return rows
    except Exception:
        return []

def readPurchasesPromotionByPKClient(pk_client):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = """   SELECT DISTINCT
                        PRODUCT.PK_PRODUCT
                    FROM
                        PRODUCT
                        LEFT JOIN CLIENT_PRODUCT ON PRODUCT.PK_PRODUCT = CLIENT_PRODUCT.PK_PRODUCT
                    WHERE CLIENT_PRODUCT.PK_CLIENT = {}
                    AND PRODUCT.PROMOTION = 1""".format(pk_client)
        cur.execute(sql)
        rows = cur.fetchall()
        conf.close()
        return rows
    except Exception:
        return []

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

def deleteProduct(pk_product):
    try:
        conf = configurationElephant()
        cur = conf.cursor()
        sql = "DELETE FROM PRODUCT WHERE PK_PRODUCT = '{}';".format(pk_product)
        cur.execute(sql)
        conf.commit()
        conf.close()
        return 1
    except:
        return 0