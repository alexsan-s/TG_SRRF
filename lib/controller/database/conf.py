import psycopg2

def configuration():
    con = psycopg2.connect(database="srrf", user="alex", password="root", host="127.0.0.1", port="5432")
    return con

def configurationElephant():
    con = psycopg2.connect(
            database="dpeswhmu", 
            user="dpeswhmu", 
            password="zVxCxEnqIf6lK3raK-uNscFDlQKfo594",
            host="tuffi.db.elephantsql.com", 
            port="5432")
    return con