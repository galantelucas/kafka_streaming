# Usar uma imagem base do Spark
FROM bitnami/spark:latest

# Trocar para o usuário root para ter permissões adequadas
USER root

# Criar o diretório /var/lib/apt/lists/partial (pode não ser necessário, mas deixado por segurança)
RUN mkdir -p /var/lib/apt/lists/partial

# Instalar dependências do Python e ferramentas de download
RUN apt-get update && \
    apt-get install -y python3 python3-pip wget && \
    rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o código Python para dentro do contêiner
COPY spark_streaming.py .

# Copiar requirements.txt para dentro do contêiner
COPY requirements.txt .

# Instalar pacotes Python necessários
RUN pip3 install --no-cache-dir -r requirements.txt

# Baixar o driver JDBC do PostgreSQL
RUN mkdir -p /opt/spark/jars && \
    wget -O /opt/spark/jars/postgresql-42.2.20.jar https://jdbc.postgresql.org/download/postgresql-42.2.20.jar

# Baixar o conector Kafka
RUN wget -O /opt/spark/jars/spark-sql-kafka-0-10_2.12-3.4.1.jar https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.4.1/spark-sql-kafka-0-10_2.12-3.4.1.jar

# Comando para executar o Spark Streaming
CMD ["spark-submit", "--master", "spark://spark-master:7077", "--jars", "/opt/spark/jars/postgresql-42.2.20.jar,/opt/spark/jars/spark-sql-kafka-0-10_2.12-3.4.1.jar", "spark_streaming.py"]
