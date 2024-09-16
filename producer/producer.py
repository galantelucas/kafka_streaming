from kafka import KafkaProducer
import json
import time
import random

def get_sale_data():
    return {
        'sale_id': random.randint(1, 1000),
        'product': random.choice(['Product A', 'Procut B', 'Product C']),
        'amount': random.uniform(10.0, 100.0)
    }

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all'
)

while True:
    sale_data = get_sale_data()
    producer.send('sales', value=sale_data)
    print(f'Sent: {sale_data}')
    time.sleep(5)
