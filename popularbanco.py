import mysql.connector
import random
from datetime import datetime, timedelta

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hospital"
    )

def populate_existing_tables():
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        # Reinicia os IDs para começar de 1
        tables_to_reset = [
            "atendimentos", "cirurgias", "especialidade_medica",
            "exames", "fornecedores", "funcionarios",
            "medicamentos", "medicos", "paciente_unidade",
            "prescricoes", "unidades_internacao"
        ]
        
        for table in tables_to_reset:
            cursor.execute(f"ALTER TABLE {table} AUTO_INCREMENT = 1")
        
        # Popula as tabelas existentes
        print("Populando tabelas existentes no banco...")

        # Tabela Medicos
        for i in range(1, 10001):
            cursor.execute("""
                INSERT INTO medicos (nome, cpf, crm, telefone)
                VALUES (%s, %s, %s, %s)
            """, (f"Médico {i}", f"{random.randint(10000000000, 99999999999)}", f"CRM-{i}", f"9{random.randint(100000000, 999999999)}"))

        # Tabela Especialidade Medica
        especialidades = ["Cardiologia", "Ortopedia", "Neurologia", "Pediatria", "Gastroenterologia", "Dermatologia", "Psiquiatria"]
        for i, especialidade in enumerate(especialidades, start=1):
            cursor.execute("""
                INSERT INTO especialidade_medica (nome, codigo, descricao, id_medico)
                VALUES (%s, %s, %s, %s)
            """, (especialidade, f"ESP-{i}", f"Descrição para {especialidade}", random.randint(1, 10000)))

        # Tabela Medicamentos
        for i in range(1, 10001):
            cursor.execute("""
                INSERT INTO medicamentos (nome, fabricante, data_validade, lote, id_fornecedor)
                VALUES (%s, %s, %s, %s, %s)
            """, (f"Medicamento {i}", f"Fabricante {random.randint(1, 50)}",
                  (datetime.now() + timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d'),
                  f"Lote-{random.randint(1000, 9999)}", random.randint(1, 10000)))

        # Tabela Fornecedores
        for i in range(1, 10001):
            cursor.execute("""
                INSERT INTO fornecedores (nome, cnpj, endereco, email, representante_comercial)
                VALUES (%s, %s, %s, %s, %s)
            """, (f"Fornecedor {i}", f"{random.randint(10000000000000, 99999999999999)}",
                  f"Endereço Fornecedor {i}", f"fornecedor{i}@hospital.com", f"Representante {i}"))

        # Tabela Cirurgias
        tipos_cirurgia = ["Cardíaca", "Ortopédica", "Neurológica", "Geral"]
        for i in range(1, 10001):
            cursor.execute("""
                INSERT INTO cirurgias (data_hora, tipo, sala, status, observacoes, id_paciente, id_medico, id_unidade)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, ((datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S'),
                  random.choice(tipos_cirurgia), f"Sala {random.randint(1, 20)}",
                  random.choice(["realizada", "cancelada", "agendada"]), f"Observação {i}",
                  random.randint(1, 10000), random.randint(1, 10000), random.randint(1, 10000)))

        # Tabela Unidades Internação
        for i in range(1, 10001):
            cursor.execute("""
                INSERT INTO unidades_internacao (nome, localizacao, capacidade_total, disponibilidade_atual)
                VALUES (%s, %s, %s, %s)
            """, (f"Unidade {i}", f"Localização {i}", random.randint(10, 50), random.randint(0, 50)))

        # Tabela Atendimentos
        for i in range(1, 10001):
            cursor.execute("""
                INSERT INTO atendimentos (data_hora, motivo_consulta, diagnostico, recomendacoes, id_paciente, id_medico)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, ((datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S'),
                  random.choice(["Dor de cabeça", "Consulta de Rotina", "Febre"]),
                  random.choice(["Saudável", "Hipertensão", "Diabetes", "Fratura"]),
                  f"Recomendação {random.randint(1000, 9999)}",
                  random.randint(1, 10000), random.randint(1, 10000)))

        # Tabela Paciente Unidade
        for i in range(1, 10001):
            cursor.execute("""
                INSERT INTO paciente_unidade (id_paciente, id_unidade, data_entrada, data_saida)
                VALUES (%s, %s, %s, %s)
            """, (random.randint(1, 10000), random.randint(1, 10000),
                  (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
                  (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')))

        # Tabela Prescrições
        for i in range(1, 10001):
            cursor.execute("""
                INSERT INTO prescricoes (id_atendimento, id_medicamento, dosagem, duracao_uso, frequencia)
                VALUES (%s, %s, %s, %s, %s)
            """, (random.randint(1, 10000), random.randint(1, 10000),
                  f"{random.randint(1, 500)}mg", random.randint(1, 30), random.randint(1, 4)))

        # Confirma as alterações no banco
        connection.commit()
        print("Tabelas existentes populadas com sucesso!")

    except Exception as e:
        connection.rollback()
        print(f"Erro ao popular tabelas: {e}")

    finally:
        cursor.close()
        connection.close()

populate_existing_tables()
