from controller.database.conf import *
import psycopg2

def createUser(name, telefone):
    conf = configuration()
    cur = conf.cursor()
    sql = "INSERT INTO tb_user(NAME, TELEFONE) VALUES('" + name + "','" + telefone + "');"
    cur.execute(sql)
    conf.commit()
    conf.close()
    print("Record inserted sucessfully")

def readUser(name):
    conf = configuration()
    cur = conf.cursor()
    sql = "SELECT ID FROM TB_USER WHERE NAME = '" + name + "';"
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows[0][0]

def readAllUser():
    conf = configuration()
    cur = conf.cursor()
    sql = "SELECT ID, NAME FROM TB_USER;"
    cur.execute(sql)
    rows = cur.fetchall()
    conf.close()
    return rows