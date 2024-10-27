# BigData_Tarea3

Análisis de Equidad Educativa mediante Apache Spark
 Una exploración de la distribución y acceso a recursos educativos

 1. Introducción al Problema y Conjunto de Datos
Problema Identificado:
- Inequidad en el acceso y distribución de recursos educativos
- Disparidades entre zonas urbanas y rurales
- Variación en la calidad educativa por estrato socioeconómico

Dataset:
- Datos de instituciones educativas
- Variables clave:
  - Ubicación (zona)
  - Estrato socioeconómico
  - Tipo de establecimiento
  - Idiomas ofrecidos
  - Matrícula contratada
  - Niveles educativos

 2. Arquitectura de la Solución en Spark

Componentes principales:
[Fuente de Datos (CSV)] → [Apache Spark] → [Análisis y Procesamiento] → [Visualización]

Capas de procesamiento:
1. Ingesta de datos (SparkSession)
2. Transformación (DataFrames)
3. Análisis (Spark SQL)
4. Presentación de resultados

 3. Explicación del Código y Tecnologías

Tecnologías Utilizadas:
- Apache Spark
- PySpark
- DataFrames
- Spark SQL

Componentes Clave del Código:

```
 Inicialización
spark = SparkSession.builder.appName('Tarea3').getOrCreate()

 Lectura de Datos
df = spark.read.format('csv')
    .option('header', 'true')
    .option('inferSchema', 'true')
    .load(file_path)

 Análisis mediante DataFrames
df.groupBy('zona').count()
df.groupBy('estrato_Socio_Economico').count()
```

 4. Demostración y Resultados

Hallazgos Principales:

1. Distribución por Zonas:
   - Mayor concentración en zonas urbanas
   - Limitada presencia en zonas rurales

2. Análisis por Estrato:
   - Distribución desigual de instituciones
   - Concentración en estratos medios y bajos

3. Oferta Educativa:
   - Variación significativa por zona
   - Limitada oferta bilingüe

 5. Actividades de Investigación

 6. Conclusiones y Aprendizajes

Conclusiones:
1. Existe una marcada desigualdad en la distribución de recursos educativos
2. La ubicación geográfica influye significativamente en el acceso a la educación
3. Hay una necesidad de fortalecer la oferta educativa en zonas rurales
4. Se requiere mayor inversión en programas bilingües

Aprendizajes Técnicos:
- Efectividad de Spark para análisis de datos educativos
- Importancia de la limpieza y preparación de datos
- Valor de la visualización para la toma de decisiones

 7. Referencias Bibliográficas

- Apache Spark. (2024). Spark SQL, DataFrames and Datasets Guide. https://spark.apache.org/docs/latest/sql-programming-guide.html
- Karau, H., & Warren, R. (2023). High Performance Spark: Best Practices for Scaling and Optimizing Apache Spark. O'Reilly Media.
- Chambers, B., & Zaharia, M. (2023). Spark: The Definitive Guide. O'Reilly Media.
