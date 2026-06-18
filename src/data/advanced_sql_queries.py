import duckdb

# Conectar a una base de datos temporal en memoria
con = duckdb.connect()

print("Conectando DuckDB al almacenamiento Parquet...")

# Definimos la consulta SQL avanzada usando triples comillas
query = """
WITH OrderedTransactions AS (
    -- 1. CTE: Agregamos una estampa de tiempo simulada basada en el ID para ordenar
    SELECT 
        transaction_id,
        user_id,
        amount,
        is_fraud,
        -- Simulamos que las transacciones ocurren secuencialmente
        epoch(to_timestamp(1718671200 + (transaction_id * 60))) AS transaction_time
    FROM '../../data/raw/transactions.parquet'
),
AnomaliesCalculated AS (
    -- 2. CTE: Aplicamos la Window Function
    SELECT 
        transaction_id,
        user_id,
        amount,
        is_fraud,
        -- Ventana: Particionamos por usuario y calculamos el promedio de sus últimas 3 transacciones
        AVG(amount) OVER(
            PARTITION BY user_id 
            ORDER BY transaction_time
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS rolling_avg_amount
    FROM OrderedTransactions
)
-- 3. Consulta Final: Calculamos la diferencia entre el monto actual y su promedio móvil
SELECT 
    transaction_id,
    user_id,
    amount,
    round(rolling_avg_amount, 2) AS rolling_avg,
    round(amount - rolling_avg_amount, 2) AS deviation,
    is_fraud
FROM AnomaliesCalculated
WHERE amount > (rolling_avg_amount * 2)
LIMIT 10;
"""

# Ejecutar la consulta y mostrar el resultado
print("Ejecutando análisis de fraude con CTEs y Window Functions...")
result = con.execute(query).df()

print("\n=== POSIBLES ANOMALÍAS DETECTADAS VÍA SQL (Monto > 2x Promedio Móvil) ===")
print(result)
