import polars as pl
import numpy as np

# Configuración de nuestra "granja" de datos
NUM_ROWS = 1_000_000  # 1 millón de transacciones
NUM_USERS = 50_000    # 50 mil clientes únicos

print(f"Sembrando {NUM_ROWS} transacciones bancarias...")

# Fijamos una semilla matemática para que los datos sean reproducibles
np.random.seed(42)

# 1. Generación vectorizada (instantánea a nivel de CPU)
user_ids = np.random.randint(1, NUM_USERS + 1, NUM_ROWS)
# Simulamos montos: la mayoría pequeños, pocos muy grandes (distribución exponencial)
amounts = np.round(np.random.exponential(scale=25.0, size=NUM_ROWS), 2)

# 2. Inyección de la variable objetivo (Target)
# Asumimos que el 1.5% de las transacciones globales son fraudulentas (desbalanceo real)
fraud_prob = 0.015
is_fraud = np.random.choice([0, 1], size=NUM_ROWS, p=[1-fraud_prob, fraud_prob])

# 3. Construcción del DataFrame en Polars
df = pl.DataFrame({
    "transaction_id": np.arange(1, NUM_ROWS + 1),
    "user_id": user_ids,
    "amount": amounts,
    "is_fraud": is_fraud
})

# 4. Guardado en formato optimizado
output_path = "../../data/raw/transactions.parquet"
df.write_parquet(output_path)

print(f"¡Cosecha lista! Datos guardados exitosamente en {output_path}")
