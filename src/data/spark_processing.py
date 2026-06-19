from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum

print("Inicializando el clúster local de PySpark...")

# 1. Crear la Sesión de Spark (El nodo maestro)
# Usamos todos los núcleos de tu CPU local con "local[*]"
spark = SparkSession.builder \
    .appName("FraudDetection_BatchProcessing") \
    .master("local[*]") \
    .getOrCreate()

# Reducimos los logs de Spark para que no inunden tu terminal
spark.sparkContext.setLogLevel("ERROR")

print("Clúster listo. Leyendo datos distribuidos...")

# 2. Lectura del archivo Parquet
# En un entorno real, esto apuntaría a un bucket de AWS S3 o Google Cloud Storage
df = spark.read.parquet("../../data/raw/transactions.parquet")

# 3. Transformación y Limpieza (Simulada)
# Verificamos si hay valores nulos en columnas críticas
print("\n--- Verificación de Calidad de Datos (Nulos) ---")
df.select([_sum(col(c).isNull().cast("int")).alias(c) for c in df.columns]).show()

# 4. Agregación Distribuida
# Calculamos el volumen total de dinero transaccionado por cada usuario
print("--- Calculando el volumen total gastado por usuario ---")
user_volume = df.groupBy("user_id") \
    .sum("amount") \
    .withColumnRenamed("sum(amount)", "total_spent") \
    .orderBy(col("total_spent").desc())

# Mostramos el Top 5 de usuarios que más dinero han movido
user_volume.show(5)

# 5. Apagar el clúster educadamente
spark.stop()
