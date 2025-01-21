import mysql.connector

# Conexão com o banco de dados
def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",      # Substitua pelo endereço do servidor MySQL
        user="root",           # Substitua pelo seu usuário
        password="",  # Substitua pela sua senha
        database="hospital"  # Substitua pelo nome do banco
    )
    return connection
