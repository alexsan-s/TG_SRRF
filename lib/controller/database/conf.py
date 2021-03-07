import psycopg2

def configuration():
    con = psycopg2.connect(database="srrf", user="alex", password="root", host="127.0.0.1", port="5432")
    return con
