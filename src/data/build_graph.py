import polars as pl
from neo4j import GraphDatabase

# 1. Configuración de conexión local a Neo4j (Levantado con Podman)
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password_segura")

print("Conectando al motor de grafos Neo4j...")
driver = GraphDatabase.driver(URI, auth=AUTH)

# 2. Extracción de datos
# Tomamos una muestra de 10,000 registros para esta prueba arquitectónica inicial
df = pl.read_parquet("data/raw/transactions.parquet").head(10000)

# 3. Diseño de la topología (Cypher)
# MERGE es el equivalente a "Insertar si no existe", evitando nodos duplicados
cypher_query = """
UNWIND $records AS record
// Crear el nodo del Usuario
MERGE (u:User {id: record.user_id})

// Crear el nodo de la Transacción con sus atributos
MERGE (t:Transaction {id: record.transaction_id})
  ON CREATE SET t.amount = record.amount, t.is_fraud = record.is_fraud

// Crear la relación direccional (Arista)
MERGE (u)-[:PERFORMED]->(t)
"""

# Convertir el DataFrame vectorizado a una lista nativa de Python
records = df.to_dicts()

print(f"Inyectando {len(records)} transacciones para construir la red...")

# 4. Transacción de Escritura en la Base de Datos
def ingest_data(tx, batch):
    tx.run(cypher_query, records=batch)

with driver.session() as session:
    session.execute_write(ingest_data, records)

driver.close()
print("¡Ingesta completada! El mapa de relaciones ha sido construido exitosamente.")
