#Importamos librerias necesarias
from pyspark.sql import SparkSession, functions as F

# 1. Definir Sesión de Spark y Cargar Dataset

# Inicializa la sesión de Spark
spark = SparkSession.builder.appName('Tarea3').getOrCreate()

# Define la ruta del archivo .csv en HDFS
file_path = 'hdfs://localhost:9000/Tarea3/rows.csv'

# Cargar dataset
df = spark.read.format('csv').option('header','true').option('inferSchema', 'true').load(file_path)

# Verificar la estructura del dataset
df.printSchema()

# 2. Exploración Inicial y Limpieza de Datos

# Mostrar nombres de columnas
print("Columnas originales:", df.columns)

# Renombrar columnas, reemplazando espacios y caracteres especiales
new_column_names = [col.replace(" ", "_").replace(".", "") for col in df.columns]
df = df.toDF(*new_column_names)

# Mostrar nombres de columnas después de renombrar
print("Columnas renombradas:", df.columns)

# Convertir columnas "POBLACIÓN_DANE" y "INDICE" a tipos numéricos
df = df.withColumn("POBLACIÓN_DANE", F.col("POBLACIÓN_DANE").cast("float"))
df = df.withColumn("INDICE", F.col("INDICE").cast("float"))

# Convertir columnas numéricas relevantes a tipo adecuado
#df = df.withColumn("AÑO", F.col("AÑO").cast("int")) \
 #      .withColumn("INDICE", F.col("INDICE").cast("float")) \
  #     .withColumn("POBLACIÓN_DANE", F.col("POBLACIÓN_DANE").cast("int"))

# Confirmar que las columnas han sido convertidas correctamente
df.printSchema()

# Descartar filas con valores nulos en columnas clave
df = df.dropna(subset=["AÑO", "INDICE", "POBLACIÓN_DANE"])
# Muestra las primeras filas del DataFrame
df.show()


# 3. Análisis Exploratorio de Datos (EDA)

# Distribución de Penetración por Municipio

# Filtrar datos para el último año disponible (ejemplo: 2023)
df_2023 = df.filter(F.col("AÑO") == 2023)

#Calcular estadísticos descriptivos del índice de penetración
df_2023.describe("INDICE").show()

# Filtrar municipios con baja penetración (por ejemplo, índice menor a 5%)
baja_conectividad = df_2023.filter(F.col("INDICE") < 5)
baja_conectividad.show()

# Correlación entre Población y Conectividad

# Calcular correlación entre población y nivel de penetración
correlacion = df_2023.stat.corr("POBLACIÓN_DANE", "INDICE")
print(f"Correlación entre población y nivel de penetración: {correlacion}")


# 4. Identificación de Municipios Prioritarios

# Definir umbrales: Baja penetración (< 5%) y alta población (> 50,000)
prioritarios = df_2023.filter((F.col("INDICE") < 5) & (F.col("POBLACIÓN_DANE") > 50000))

# Mostrar los municipios prioritarios
prioritarios.select("DEPARTAMENTO", "MUNICIPIO", "POBLACIÓN_DANE", "INDICE").show()


# 5. Visualización de Resultados

# Convertir a Pandas para visualización
prioritarios_pd = prioritarios.toPandas()
# Graficar
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(prioritarios_pd["MUNICIPIO"], prioritarios_pd["INDICE"], color="orange")
plt.xticks(rotation=90)
plt.xlabel("Municipio")
plt.ylabel("Índice de Penetración")
plt.title("Municipios con Baja Penetración de Internet")
plt.show()
