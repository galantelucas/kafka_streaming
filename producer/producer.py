from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime,timedelta

# Função para gerar coordenadas aleatórias dentro de continentes
def generate_random_coordinates():
    latitudes = {
        "North America": (15.0, 75.0),
        "South America": (-55.0, 15.0),
        "Europe": (35.0, 70.0),
        "Africa": (-35.0, 37.0),
        "Asia": (5.0, 55.0),
        "Oceania": (-50.0, -10.0)
    }
    
    longitudes = {
        "North America": (-170.0, -50.0),
        "South America": (-80.0, -35.0),
        "Europe": (-10.0, 50.0),
        "Africa": (-20.0, 50.0),
        "Asia": (50.0, 150.0),
        "Oceania": (110.0, 180.0)
    }
    
    # Escolhe um continente aleatório
    continent = random.choice(list(latitudes.keys()))
    
    # Gera coordenadas aleatórias dentro dos limites do continente escolhido
    latitude = round(random.uniform(latitudes[continent][0], latitudes[continent][1]), 6)
    longitude = round(random.uniform(longitudes[continent][0], longitudes[continent][1]), 6)
    
    return latitude, longitude

# Função para buscar dados de venda
def get_sale_data():
    latitude, longitude = generate_random_coordinates()  # Usa a função atualizada
    
    # Adiciona a data e hora atual no formato ISO 8601 periodo máximo de 1 ano
    random_days = random.randint(0, 365)
    sale_date = (datetime.now() - timedelta(days=random_days)).strftime('%Y-%m-%d')
    
    return {
        'sale_id': random.randint(1, 1000),
        'product': random.choice(['Product A', 'Product B', 'Product C']),
        'amount': round(random.uniform(10.0, 100.0), 2),  # Arredonda o valor para 2 casas decimais
        'latitude': latitude,
        'longitude': longitude,
        'sale_date': sale_date  # Adiciona o campo de data
    }

# Configuração do Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all'
)

# Loop de envio de mensagens para o Kafka
while True:
    sale_data = get_sale_data()
    producer.send('sales', value=sale_data)
    print(f'Sent: {sale_data}')
    time.sleep(5)
