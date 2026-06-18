import polars as pl

# 1. Leer el archivo Parquet (Polars lo hace de forma casi instantánea)
df = pl.read_parquet("../../data/raw/transactions.parquet")

print("=== INSPECCIÓN DE ARQUITECTURA DE DATOS ===")
print(f"Dimensiones de la matriz: {df.shape[0]:,} filas x {df.shape[1]} columnas\n")

print("--- Esquema de Datos (Tipos de Datos Correctos) ---")
print(df.schema)
print("")

print("--- Muestra de las primeras 5 transacciones ---")
print(df.head(5))
print("")

print("--- Validación del Desbalanceo de Clases (Métrica de Fraude) ---")
# Agrupamos por la columna objetivo para calcular volumen y porcentaje
analisis_fraude = df.group_by("is_fraud").agg(
    pl.len().alias("total_casos"),
    (pl.len() / len(df) * 100).round(2).alias("porcentaje")
)

print(analisis_fraude)
