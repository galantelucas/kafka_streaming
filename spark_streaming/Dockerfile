# Usar uma imagem base do Spark
FROM bitnami/spark:latest

# Trocar para o usuário root para ter permissões adequadas
USER root

# Criar o diretório /var/lib/apt/lists/partial (pode não ser necessário, mas deixado por segurança)
RUN mkdir -p /var/lib/apt/lists/partial

# Instalar dependências do Python e ferramentas de download
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ajustar permissões do diretório tmp do Spark
RUN chmod -R 777 /opt/bitnami/spark/tmp

# Ajustar permissões do diretório de configuração do Spark
RUN chmod -R 777 /opt/bitnami/spark/conf

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o código Python para dentro do contêiner
COPY spark_streaming.py .

# Copiar requirements.txt para dentro do contêiner
COPY requirements.txt .

# Instalar pacotes Python necessários
RUN pip3 install --no-cache-dir -r requirements.txt

# Criar diretório para os JARs do Spark
RUN mkdir -p /opt/spark/jars

# Copiar o driver JDBC do PostgreSQL
COPY postgresql-42.2.20.jar /opt/spark/jars/

# Copiar o conector Kafka
COPY spark-sql-kafka-0-10_2.12-3.5.3.jar /opt/spark/jars/

# Copiar o JAR do Kafka Client
COPY kafka-clients-3.8.0.jar /opt/spark/jars/

# Criar um usuário não-root para executar o Spark
RUN useradd -m sparkuser

# Alterar a propriedade dos arquivos e diretórios relevantes
RUN chown -R sparkuser:sparkuser /opt/bitnami/spark

# Mudar para o usuário não-root
USER sparkuser

# Comando para executar o Spark Streaming
CMD ["spark-submit", "--master", "spark://spark-master:7077", "--jars", "/opt/spark/jars/postgresql-42.2.20.jar,/opt/spark/jars/spark-sql-kafka-0-10_2.12-3.5.3.jar,/opt/spark/jars/kafka-clients-3.8.0.jar", "spark_streaming.py"]
