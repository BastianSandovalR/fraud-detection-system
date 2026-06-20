from neo4j import GraphDatabase

# Configuración de conexión
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password_segura")

print("Conectando al motor GDS de Neo4j...")
driver = GraphDatabase.driver(URI, auth=AUTH)

# Consultas Cypher para la tubería analítica
QUERIES = {
    # 1. Proyectar el grafo en memoria RAM
    "project": """
        CALL gds.graph.project(
            'fraudGraph',
            ['User', 'Transaction'],
            'PERFORMED'
        )
    """,
    # 2. Ejecutar PageRank con Damping Factor de 0.85 y escribir el score en la base de datos
    "pagerank": """
        CALL gds.pageRank.write(
            'fraudGraph',
            {
                maxIterations: 20,
                dampingFactor: 0.85,
                writeProperty: 'pagerank_score'
            }
        )
        YIELD nodePropertiesWritten, ranIterations
        RETURN nodePropertiesWritten, ranIterations
    """,
    # 3. Limpiar la RAM destruyendo la proyección
    "cleanup": """
        CALL gds.graph.drop('fraudGraph')
    """
}

def run_gds_pipeline(tx):
    # Paso 1: Proyección
    print("Creando proyección en memoria RAM...")
    tx.run(QUERIES["project"])
    
    # Paso 2: Cálculo matemático
    print("Calculando PageRank y aplicando Damping Factor (0.85)...")
    result = tx.run(QUERIES["pagerank"]).single()
    print(f"Puntuaciones escritas en {result['nodePropertiesWritten']} nodos tras {result['ranIterations']} iteraciones.")
    
    # Paso 3: Limpieza
    print("Liberando memoria RAM...")
    tx.run(QUERIES["cleanup"])

# Ejecución de la transacción
with driver.session() as session:
    session.execute_write(run_gds_pipeline)

driver.close()
print("¡Ingeniería de características topológicas completada!")
