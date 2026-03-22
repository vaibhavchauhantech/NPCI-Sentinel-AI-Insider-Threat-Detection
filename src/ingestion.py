# src/ingestion.py
# Real-time Log Ingestion Module (Objective 3: Dataset Processing) [cite: 23, 24]
import json
try:
    from kafka import KafkaConsumer
except ImportError:
    KafkaConsumer = None

def start_kafka_stream(topic='npci_logs', server='localhost:9092'):
    """Simulates real-time ingestion from a Kafka topic """
    if KafkaConsumer is None:
        return "Kafka library not found. Install 'kafka-python'."
    
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[server],
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    print(f"📡 Sentinel: Listening to Kafka topic '{topic}'...")
    # This would feed directly into the detection engine [cite: 25]
    return consumer