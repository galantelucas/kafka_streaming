from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, NumericType, DateType
import os
import psycopg2

# Função para criar a tabela sales no PostgreSQL, caso não exista


def create_sales_table():
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


# Configurações do Spark
spark = SparkSession.builder \
    .appName("SalesStreaming") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

# Criar a tabela sales no PostgreSQL
create_sales_table()

# Definições do esquema do DataFrame
schema = StructType([
    StructField("product", StringType(), True),
    StructField("amount", NumericType(), True),
    StructField("latitude", NumericType(), True),
    StructField("longitude", NumericType(), True),
    StructField("sale_date", DateType(), True)
])

# Lendo dados do Kafka
sales_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", os.environ['KAFKA_BROKER']) \
    .option("subscribe", os.environ['KAFKA_TOPIC']) \
    .load()

# Deserializando dados do Kafka
sales_df = sales_stream \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Função para inserir dados no PostgreSQL


def upsert_to_postgres(df, epoch_id):
    try:
        df.write \
            .format("jdbc") \
            .option("url", f"jdbc:postgresql://{os.environ['POSTGRES_HOST']}:5432/{os.environ['POSTGRES_DB']}") \
            .option("dbtable", "sales") \
            .option("user", os.environ['POSTGRES_USER']) \
            .option("password", os.environ['POSTGRES_PASSWORD']) \
            .mode("append") \
            .save()
    except Exception as e:
        print(f"Erro ao inserir dados no PostgreSQL: {e}")


# Iniciando o stream
query = sales_df \
    .writeStream \
    .foreachBatch(upsert_to_postgres) \
    .outputMode("append") \
    .start()

# Esperando a conclusão da execução do stream
try:
    query.awaitTermination(5)
except KeyboardInterrupt:
    print("Stream interrompido pelo usuário.")
finally:
    spark.stop()
