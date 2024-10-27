import time
import json
import random
from kafka import KafkaProducer

def generate_sensor_data():
    return {
        "sensor_id": random.randint(1, 10),
        "temperature": round(random.uniform(20, 30), 2),      # Temperatura en °C
        "humidity": round(random.uniform(30, 70), 2),         # Humedad en %
        "pressure": round(random.uniform(980, 1020), 1),      # Presión atmosférica en hPa
        "air_quality": random.randint(0, 500),                # Índice de calidad del aire (AQI)
        "timestamp": int(time.time())
    }

def get_air_quality_level(aqi):
    """Función auxiliar para interpretar el nivel de calidad del aire"""
    if aqi <= 50:
        return "Bueno"
    elif aqi <= 100:
        return "Moderado"
    elif aqi <= 150:
        return "Insalubre para grupos sensibles"
    elif aqi <= 200:
        return "Insalubre"
    elif aqi <= 300:
        return "Muy insalubre"
    else:
        return "Peligroso"

# Configuración del productor Kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Bucle principal para generar y enviar datos
try:
    while True:
        # Generar datos del sensor
        sensor_data = generate_sensor_data()

        # Enviar datos a Kafka
        producer.send('sensor_data', value=sensor_data)

        # Imprimir datos con interpretación de la calidad del aire
        print(f"Sent: {sensor_data}")
        print(f"Calidad del aire: {get_air_quality_level(sensor_data['air_quality'])}")
        print("-" * 50)

        # Esperar 1 segundo antes de la siguiente lectura
        time.sleep(1)

except KeyboardInterrupt:
    print("\nDetención del productor solicitada por el usuario")
    producer.close()
except Exception as e:
    print(f"\nError: {e}")
    producer.close()
