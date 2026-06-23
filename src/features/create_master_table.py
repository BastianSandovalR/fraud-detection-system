import polars as pl
from neo4j import GraphDatabase

# 1. Configuración de conexión local a Neo4j
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password_segura")

print("1. Conectando a Neo4j para extraer la inteligencia topológica...")
driver = GraphDatabase.driver(URI, auth=AUTH)

# Consulta Cypher para traer solo a los usuarios y su score de riesgo
extract_query = """
MATCH (u:User)
WHERE u.pagerank_score IS NOT NULL
RETURN u.id AS user_id, u.pagerank_score AS pagerank_score
"""

def fetch_scores(tx):
    result = tx.run(extract_query)
    # Extraemos los datos en formato de lista de diccionarios
    return [record.data() for record in result]

with driver.session() as session:
    graph_features = session.execute_read(fetch_scores)

driver.close()
print(f"   -> ¡Extraídos los scores de {len(graph_features)} usuarios desde el grafo!")

# 2. Carga de los Datos Tabulares Base
print("2. Cargando la base de transacciones crudas desde Parquet (Muestra de 10k)...")
# TRUCO DE LA OPCIÓN A: Limitamos la tabla base a las primeras 10,000 filas 
# para que coincida con lo que inyectamos en Neo4j en la Fase 1
df_raw = pl.read_parquet("data/raw/transactions.parquet").head(10000)

# Convertimos la lista de diccionarios de Neo4j a un DataFrame de Polars ultra rápido
df_scores = pl.DataFrame(graph_features)

# 3. El Gran Cruce (Feature Merge)
# Unimos la tabla base con los scores usando 'user_id' como llave maestra
print("3. Realizando el cruce relacional (JOIN)...")
df_master = df_raw.join(df_scores, on="user_id", how="left")

# Llenamos los nulos con 0 en caso de que algún usuario no haya entrado al cálculo del grafo
df_master = df_master.with_columns(
    pl.col("pagerank_score").fill_null(0.0)
)

print("\n--- Top 5 Transacciones con Mayor Riesgo Topológico (PageRank) ---")
# Ordenamos la tabla de mayor a menor score para visualizar las anomalías en la terminal
df_master_sorted = df_master.sort("pagerank_score", descending=True)
print(df_master_sorted.head(5))

# 4. Guardado para el Modelo Predictivo
output_path = "data/processed/master_table.parquet"
print(f"\n4. Guardando la Tabla Maestra en: {output_path}")
df_master.write_parquet(output_path)

print("¡Proceso completado! Los datos están listos para la Inteligencia Artificial.")
