import requests
import concurrent.futures
import time
import random

# La dirección de tu contenedor blindado
API_URL = "http://localhost:8000/predict"

# Configuración de la prueba: 1000 transacciones disparadas por 50 usuarios simultáneos
TOTAL_TRANSACTIONS = 1000
CONCURRENT_USERS = 50

def send_transaction(tx_id):
    """Simula una transacción aleatoria enviada a la API."""
    payload = {
        "amount": round(random.uniform(5.0, 3000.0), 2),
        "pagerank_score": round(random.uniform(0.15, 0.99), 4)
    }
    
    try:
        start_time = time.time()
        # Disparamos la petición HTTP al contenedor
        response = requests.post(API_URL, json=payload, timeout=2)
        latency = (time.time() - start_time) * 1000 # Convertir a milisegundos
        
        return response.status_code, latency, payload["amount"]
    except Exception as e:
        return 500, 0, str(e)

print(f"🚀 Iniciando ataque simulado contra el contenedor de Fraude...")
print(f"-> Disparando {TOTAL_TRANSACTIONS} transacciones con {CONCURRENT_USERS} usuarios concurrentes.\n")

start_test_time = time.time()
latencies = []
success_count = 0
fraud_alerts = 0

# Usamos ThreadPoolExecutor para simular la concurrencia real (múltiples hilos atacando a la vez)
with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_USERS) as executor:
    # Mapeamos la función a los 1000 IDs de transacción
    results = executor.map(send_transaction, range(TOTAL_TRANSACTIONS))
    
    for status, latency, amount in results:
        if status == 200:
            success_count += 1
            latencies.append(latency)
            # Simulamos que detectó fraude si la latencia es registrada y el monto supera cierto umbral (según nuestra lógica de API)
            if amount > 500 and random.random() > 0.8: # Solo para simular alertas visuales
                 fraud_alerts += 1

total_time = time.time() - start_test_time

# Resultados Analíticos
if latencies:
    avg_latency = sum(latencies) / len(latencies)
    max_latency = max(latencies)
else:
    avg_latency = max_latency = 0

print("=== 📊 REPORTE DE LA PRUEBA DE ESTRÉS ===")
print(f"Transacciones Exitosas: {success_count} / {TOTAL_TRANSACTIONS}")
print(f"Tiempo Total de la Prueba: {total_time:.2f} segundos")
print(f"Latencia Promedio: {avg_latency:.2f} ms por transacción")
print(f"Latencia Máxima (Peor caso): {max_latency:.2f} ms")
print(f"Tasa de Procesamiento: {TOTAL_TRANSACTIONS / total_time:.0f} transacciones / segundo")
print("=========================================")

if success_count == TOTAL_TRANSACTIONS and avg_latency < 100:
    print("\n✅ RESULTADO: ¡Tu contenedor de FastAPI es un tanque! Aprobó la prueba de grado bancario.")
else:
    print("\n⚠️ RESULTADO: El contenedor sobrevivió, pero hay cuello de botella. Necesitaríamos escalar los workers de Uvicorn.")
