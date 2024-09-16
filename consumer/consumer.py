import psycopg2
from kafka import KafkaConsumer
import json
from time import sleep
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para esperar o PostgreSQL estar pronto
def wait_for_postgres():
    while True:
        try:
            conn = psycopg2.connect(
                host='db',
                database='sales_db',
                user='postgres',
                password='postgres'
            )
            conn.close()
            break
        except psycopg2.OperationalError:
            logging.info("PostgreSQL not available yet. Waiting...")
            sleep(5)

# Esperar o PostgreSQL estar pronto
wait_for_postgres()

# Configurações de conexão com o banco de dados PostgreSQL
conn = psycopg2.connect(
    host="db",  # Nome do serviço no Docker
    database="sales_db",  # Nome do banco de dados
    user="postgres",  # Usuário
    password="postgres"  # Senha
)
cur = conn.cursor()

# Criando a tabela sales, caso não exista
cur.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        sale_id SERIAL PRIMARY KEY,
        product VARCHAR(255),
        amount NUMERIC
    )
''')
conn.commit()

# Configurando o consumidor do Kafka
consumer = KafkaConsumer(
    'sales',        # Nome do tópico
    bootstrap_servers=['kafka:9092'],  # Nome do serviço Kafka no Docker
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Consumindo mensagens e inserindo no banco de dados
try:
    for message in consumer:
        data = message.value
        try:
            cur.execute(
                "INSERT INTO sales (product, amount) VALUES (%s, %s)",
                (data['product'], data['amount'])
            )
            conn.commit()
            logging.info(f"Mensagem processada: {data}")
        except Exception as e:
            logging.error(f"Erro ao inserir dados no banco: {e}")
finally:
    cur.close()
    conn.close()
