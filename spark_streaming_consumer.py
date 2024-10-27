from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, max, min, from_unixtime
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, TimestampType, LongType
import logging

# Configurar Spark
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Definir el esquema
schema = StructType([
    StructField("sensor_id", IntegerType()),
    StructField("temperature", FloatType()),
    StructField("humidity", FloatType()),
    StructField("pressure", FloatType()),
    StructField("air_quality", IntegerType()),
    StructField("timestamp", LongType())
])

# Leer de Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor_data") \
    .load()

# Parsear JSON y convertir timestamp
parsed_df = df \
    .select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("timestamp", from_unixtime(col("timestamp")).cast(TimestampType()))

# Calcular estadísticas
windowed_stats = parsed_df \
    .groupBy(
        window(col("timestamp"), "1 minute"),
        "sensor_id"
    ) \
    .agg(
        avg("temperature").alias("avg_temp"),
        avg("humidity").alias("avg_humidity"),
        avg("pressure").alias("avg_pressure"),
        avg("air_quality").alias("avg_air_quality"),
        max("temperature").alias("max_temp"),
        max("humidity").alias("max_humidity"),
        max("pressure").alias("max_pressure"),
        max("air_quality").alias("max_air_quality"),
        min("temperature").alias("min_temp"),
        min("humidity").alias("min_humidity"),
        min("pressure").alias("min_pressure"),
        min("air_quality").alias("min_air_quality")
    )

# Función para interpretar calidad del aire
def interpret_air_quality(aqi):
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

# Registrar UDF
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

interpret_air_quality_udf = udf(interpret_air_quality, StringType())

# Agregar interpretación de calidad del aire
windowed_stats = windowed_stats \
    .withColumn("air_quality_level", interpret_air_quality_udf(col("avg_air_quality")))

# Escribir resultados
query = windowed_stats \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 1000) \
    .start()

# Esperar terminación
query.awaitTermination()
