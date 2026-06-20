from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import xgboost as xgb

# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="Fraud Detection API", 
    description="Motor de Inferencia para Detección de Fraude en Tiempo Real",
    version="1.0"
)

# 1. Definir el Esquema de Entrada (Contrato de Datos)
class TransactionData(BaseModel):
    amount: float
    pagerank_score: float

# Nota de Arquitectura: En un entorno de producción, aquí conectaríamos con 
# el Model Registry de MLflow para descargar el último modelo en estado "Production".
# Por ahora, dejaremos la estructura preparada para hacer la predicción.

@app.post("/predict")
def predict_fraud(transaction: TransactionData):
    """
    Recibe una transacción, la transforma en un vector matemático y 
    devuelve la probabilidad de fraude.
    """
    # Transformar el JSON entrante a un formato tabular que XGBoost entiende
    df = pd.DataFrame([transaction.model_dump()])
    
    # --- ESPACIO PARA EL MODELO REAL ---
    # Aquí iría: proba = model.predict_proba(df)[0][1]
    
    # Simulamos la lógica del modelo para esta prueba arquitectónica:
    # Si el monto es alto y el score topológico es sospechoso, disparamos la alerta
    risk_score = 0.92 if (transaction.amount > 500 and transaction.pagerank_score > 0.5) else 0.03
    is_fraud = int(risk_score > 0.80)
    
    return {
        "status": "success",
        "is_fraud": is_fraud,
        "risk_probability": risk_score,
        "features_processed": list(df.columns)
    }

@app.get("/health")
def health_check():
    """Endpoint de monitoreo para Kubernetes/Docker"""
    return {"status": "healthy", "model": "xgboost-fraud-v1"}
