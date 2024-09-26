from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DateType
import os
import psycopg2
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)

# Função para criar a tabela sales no PostgreSQL, caso não exista


def create_sales_table():
    try:
        conn = psycopg2.connect(
            host=os.environ['POSTGRES_HOST'],
            database=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD']
        )
        cur = conn.cursor()
        cur.execute(''' 
            CREATE TABLE IF NOT EXISTS sales (
                sale_id SERIAL PRIMARY KEY,
                product VARCHAR(20),
                amount NUMERIC,
                latitude NUMERIC,
                longitude NUMERIC,
                sale_date DATE
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        logging.info("Tabela 'sales' criada ou já existe.")
    except Exception as e:
        logging.error(f"Erro ao criar tabela no PostgreSQL: {e}")

# Função para configurar o Spark


def create_spark_session():
    try:
        spark = SparkSession.builder \
            .appName("SalesStreaming") \
            .config("spark.sql.shuffle.partitions", "2") \
            .getOrCreate()
        logging.info("Spark session criada com sucesso.")
        return spark
    except Exception as e:
        logging.error(f"Erro ao criar Spark session: {e}")
        raise  # Propaga a exceção para interromper a execução

# Função para inserir dados no PostgreSQL


def upsert_to_postgres(df, epoch_id):
    try:
        df.write \
            .format("jdbc") \
            .option("url", f"jdbc:postgresql://{os.environ['POSTGRES_HOST']}:5432/{os.environ['POSTGRES_DB']}") \
            .option("dbtable", "sales") \
            .option("user", os.environ['POSTGRES_USER']) \
            .option("password", os.environ['POSTGRES_PASSWORD']) \
            .option("batchsize", "1000") \
            .mode("append") \
            .save()
        logging.info(f"Batch de dados inserido no PostgreSQL: {epoch_id}")
    except Exception as e:
        logging.error(f"Erro ao inserir dados no PostgreSQL: {e}")


# Configurações do Spark
spark = create_spark_session()

# Criar a tabela sales no PostgreSQL
create_sales_table()

# Definições do esquema do DataFrame
schema = StructType([
    StructField("product", StringType(), True),
    # Usando DoubleType para valores decimais
    StructField("amount", DoubleType(), True),
    StructField("latitude", DoubleType(), True),
    StructField("longitude", DoubleType(), True),
    StructField("sale_date", DateType(), True)
])

# Lendo dados do Kafka
try:
    sales_stream = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", os.environ['KAFKA_BROKER']) \
        .option("subscribe", os.environ['KAFKA_TOPIC']) \
        .load()
    logging.info("Dados lidos do Kafka com sucesso.")
except Exception as e:
    logging.error(f"Erro ao ler dados do Kafka: {e}")

# Deserializando dados do Kafka
try:
    sales_df = sales_stream \
        .selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")
    logging.info("Dados do Kafka deserializados com sucesso.")
except Exception as e:
    logging.error(f"Erro ao deserializar dados do Kafka: {e}")

# Iniciando o stream
try:
    query = sales_df \
        .writeStream \
        .foreachBatch(upsert_to_postgres) \
        .outputMode("append") \
        .start()

    # Esperando a conclusão da execução do stream
    query.awaitTermination()  # Para execução contínua
except KeyboardInterrupt:
    logging.info("Stream interrompido pelo usuário.")
except Exception as e:
    logging.error(f"Erro durante a execução do stream: {e}")
finally:
    spark.stop()
    logging.info("Spark session encerrada.")
