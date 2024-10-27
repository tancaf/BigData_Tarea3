# Importamos librerías necesarias
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Inicializa la sesión de Spark
spark = SparkSession.builder.appName('Tarea3').getOrCreate()

# Define la ruta del archivo .csv en HDFS
file_path = 'hdfs://localhost:9000/Tarea3/rows.csv'

# Lee el archivo .csv
df = spark.read.format('csv').option('header', 'true').option('inferSchema', 'true').load(file_path)

# Imprimimos el esquema
df.printSchema()

# 1. Conteo de las opciones en la columna 'calendario'
print("Conteo de las opciones en la columna 'calendario':\n")
df.groupBy('calendario').count().show()

# 2. Conteo de los 5 tipos de 'propiedad_Planta_Fisica' más comunes
print("Conteo de los 5 tipos de 'propiedad_Planta_Fisica' más comunes:\n")
df.groupBy('propiedad_Planta_Fisica').count().orderBy('count', ascending=False).show(5)

# 3. Relación entre 'nombreestablecimiento' con 'niveles' y 'idiomas'
print("Relación entre 'nombreestablecimiento' con 'niveles' y 'idiomas':\n")
df.select('nombreestablecimiento', 'niveles', 'idiomas').distinct().show(truncate=False)

# 4. Conteo de 'tipo_Establecimiento' en relación con idiomas inglés y español
print("Conteo de 'tipo_Establecimiento' con idiomas inglés y español:\n")
df.filter(df.idiomas.isin('INGLÉS', 'ESPAÑOL'))\
    .groupBy('tipo_Establecimiento', 'idiomas')\
    .count()\
    .show()

# 5. Relación entre 'nombreestablecimiento' y 'jornadas'
print("Relación entre 'nombreestablecimiento' y 'jornadas':\n")
df.select('nombreestablecimiento', 'jornadas').distinct().show(truncate=False)

# 6. Conteo de las diferentes 'zonas'
print("Conteo de las diferentes 'zonas':\n")
df.groupBy('zona').count().show()

# 7. Conteo de 'secretaria' y número total de establecimientos por secretaria
print("Conteo de establecimientos por secretaria:\n")
df.groupBy('secretaria').count().orderBy('count', ascending=False).show()

# 8. Conteo de 'tipo_Establecimiento' por 'zona'
print("Conteo de 'tipo_Establecimiento' por 'zona':\n")
df.groupBy('zona', 'tipo_Establecimiento').count().show()

# 9. Conteo de instituciones por 'estrato_Socio_Economico'
print("Conteo de instituciones por 'estrato_Socio_Economico':\n")
df.groupBy('estrato_Socio_Economico').count().show()

# 10. Media de 'matricula_Contratada' por 'tipo_Establecimiento'
print("Media de 'matricula_Contratada' por 'tipo_Establecimiento':\n")
df.groupBy('tipo_Establecimiento').agg(F.avg('matricula_Contratada').alias('media_matricula')).show()

# 11. Conteo de 'genero' por 'secretaria'
print("Conteo de 'genero' por 'secretaria':\n")
df.groupBy('secretaria', 'genero').count().show()

# 12. Total de instituciones por 'nombre_Rector'
print("Total de instituciones por 'nombre_Rector':\n")
df.groupBy('nombre_Rector').count().orderBy('count', ascending=False).show(10)

# 13. Conteo de 'etnias' por 'zona'
print("Conteo de 'etnias' por 'zona':\n")
df.groupBy('zona', 'etnias').count().show(truncate=False)

