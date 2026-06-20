import polars as pl
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, average_precision_score
import mlflow
import mlflow.xgboost

print("1. Cargando la Tabla Maestra...")
df = pl.read_parquet("data/processed/master_table.parquet")

# 2. Preparación de los Datos
# Separar características (X) y la variable objetivo (y)
# Excluimos transaction_id y user_id porque son identificadores, no patrones matemáticos
X = df.drop(["transaction_id", "user_id", "is_fraud"]).to_pandas()
y = df["is_fraud"].to_pandas()

print("2. Dividiendo datos en Entrenamiento y Prueba...")
# stratify=y garantiza que el 1.5% de fraude se mantenga exacto en ambos conjuntos
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Matemáticas para el Desbalanceo Severo
# scale_pos_weight le dice a XGBoost: "Equivocarte en un fraude cuesta X veces más que en un caso normal"
conteo_negativos = len(y_train) - sum(y_train)
conteo_positivos = sum(y_train)
scale_pos_weight = conteo_negativos / conteo_positivos

print(f"-> Penalización por fraude no detectado fijada en: {scale_pos_weight:.2f}x")

print("3. Entrenando XGBoost con Registro Científico de MLflow...")
# Configurar el experimento en MLflow
mlflow.set_experiment("Fraud_Detection_XGBoost")

# Iniciar la grabación del experimento
with mlflow.start_run():
    # Definir los hiperparámetros de arquitectura
    params = {
        "objective": "binary:logistic",
        "max_depth": 5,
        "learning_rate": 0.1,
        "scale_pos_weight": scale_pos_weight,
        "eval_metric": "aucpr"
    }
    
    # MLflow: Registrar hiperparámetros
    mlflow.log_params(params)
    
    # Instanciar y Entrenar
    clf = xgb.XGBClassifier(**params)
    clf.fit(X_train, y_train)
    
    print("4. Evaluando el modelo...")
    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)[:, 1]
    
    # Evaluar con Average Precision (AUPRC) - La métrica más estricta para fraude
    avg_precision = average_precision_score(y_test, y_proba)
    print(f"\n=== RESULTADOS DEL MODELO ===")
    print(f"Average Precision (AUPRC): {avg_precision:.4f}")
    print("\nReporte de Clasificación:")
    print(classification_report(y_test, y_pred))
    
    # MLflow: Registrar métricas y guardar el modelo físico
    mlflow.log_metric("average_precision", avg_precision)
    mlflow.xgboost.log_model(clf, "xgboost-fraud-model")
    
print("¡Entrenamiento y registro científico completados exitosamente!")
