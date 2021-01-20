from pymongo import MongoClient


# Conecção do banco de dados
def connection():
    return MongoClient('localhost', 27017)

# Criando o banco de dados
def createDatabase():
    dbs = connection()
    database = dbs.tg
    return database

# criando a tabela do banco
# recebendo o parametro json
def createTableUSer(userJson):
    database = createDatabase()
    user = database.user
    user.insert_one(userJson).inserted_id

# procurar o usuario pelo ID
def findId(id):
    database = createDatabase()
    user = database.user
    data = user.find_one({"_id": id})
    print(data)


user = {
    "_id": 1,
    "nome": "Alexsander da Silva"
}
# createTableUSer(user)
print('foi')
findId(1)