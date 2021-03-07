from controller.database.conf import *
import psycopg2

# ! CREATE TABLES

def createUser(name, telefone, cpf):
    try:
        conf = configuration()
        cur = conf.cursor()
        sql = "INSERT INTO tb_user(NAME, TELEFONE, CPF) VALUES('{}','{}','{}');".format(name, telefone, cpf)
        cur.execute(sql)
        conf.commit()
        conf.close()
        print("Record inserted sucessfully")
        return 1
    except:
        return 0

# ! READ TABLES

def readUser(cpf):
    conf = configuration()
    cur = conf.cursor()
    sql = "SELECT ID FROM TB_USER WHERE CPF = '" + cpf + "';"
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows[0][0]

def readAllUser():
    conf = configuration()
    cur = conf.cursor()
    sql = "SELECT ID, NAME, TELEFONE, CPF FROM TB_USER;"
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows

# ! DROP TABLE
def deleteUser(cod):
    conf = configuration()
    cur = conf.cursor()
    sql = "DELETE FROM TB_USER WHERE ID = '{}';".format(cod)
    cur.execute(sql)
    conf.commit()
    conf.close()
    print('deletado')
