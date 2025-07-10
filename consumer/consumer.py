import psycopg2
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
from time import sleep
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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

# Função para esperar o Kafka estar pronto


def wait_for_kafka(topic):
    RETRIES = 10
    for attempt in range(RETRIES):
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=['kafka:9092'],
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            return consumer
        except NoBrokersAvailable:
            logging.warning(
                f"[Tentativa {attempt+1}/{RETRIES}] Kafka não disponível. Aguardando...")
            sleep(5)
    logging.error("Kafka não respondeu após várias tentativas. Encerrando.")
    exit(1)


# Esperar PostgreSQL e Kafka
wait_for_postgres()
consumer = wait_for_kafka('sales')

# Conexão com o banco de dados
conn = psycopg2.connect(
    host="db",
    database="sales_db",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()

# Criando a tabela sales, caso não exista
cur.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        sale_id SERIAL PRIMARY KEY,
        product VARCHAR(255),
        amount NUMERIC,
        latitude NUMERIC,
        longitude NUMERIC,
        sale_date DATE
    )
''')
conn.commit()

# Consumindo mensagens do Kafka
try:
    for message in consumer:
        data = message.value
        try:
            cur.execute(
                "INSERT INTO sales (product, amount, latitude, longitude, sale_date) VALUES (%s, %s, %s, %s, %s)",
                (data['product'], data['amount'], data['latitude'],
                 data['longitude'], data['sale_date'])
            )
            conn.commit()
            logging.info(f"Mensagem processada: {data}")
        except Exception as e:
            logging.error(f"Erro ao inserir dados no banco: {e}")
finally:
    cur.close()
    conn.close()
