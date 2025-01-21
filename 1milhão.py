import mysql.connector
from datetime import datetime, timedelta

# Conexão com o banco de dados
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",  # Endereço do servidor
        user="root",       # Usuário do banco de dados
        password="",       # Senha do banco
        database="hospital"  # Nome do banco de dados
    )

def populate_pacientes_sequencial():
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        print("Populando a tabela Pacientes com 1 milhão de registros...")
        batch_size = 10000  # Inserir registros em lotes
        total_records = 1000000  # Total de registros

        # Reinicia o ID para começar de 1
        cursor.execute("ALTER TABLE pacientes AUTO_INCREMENT = 1")

        for batch_start in range(1, total_records + 1, batch_size):
            records = []
            for i in range(batch_start, batch_start + batch_size):
                nome = f"Paciente {i}"
                cpf = f"{i:011d}"  # Gera um CPF sequencial (11 dígitos com zero à esquerda)
                data_nascimento = (datetime.now() - timedelta(days=i % 30000)).strftime('%Y-%m-%d')  # Data variável
                endereco = f"Endereço {i}"
                telefone = f"9{i % 100000000:08d}"  # Telefone com 8 dígitos variáveis
                contato_emergencia = f"Contato {i}"
                records.append((nome, cpf, data_nascimento, endereco, telefone, contato_emergencia))

            # Inserir o lote no banco
            query = """
            INSERT INTO pacientes (nome, cpf, data_nascimento, endereco, telefone, contato_emergencia)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(query, records)
            connection.commit()
            print(f"Lote {batch_start // batch_size + 1} inserido com sucesso!")

    except Exception as e:
        connection.rollback()
        print(f"Erro ao popular tabela: {e}")
    finally:
        cursor.close()
        connection.close()

populate_pacientes_sequencial()
