from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# 1. Configuración de la "personalidad" del robot
default_args = {
    'owner': 'mlops_architect',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 2. Definición del Grafo (DAG)
# Le decimos que se ejecute todos los días a las 3:00 AM ('0 3 * * *' en formato Cron)
with DAG(
    'fraud_model_daily_retraining',
    default_args=default_args,
    description='Pipeline automático para extraer datos topológicos y reentrenar XGBoost',
    schedule_interval='0 3 * * *',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['fraude', 'mlops', 'produccion'],
) as dag:

    # 3. Tarea A: Crear la Tabla Maestra (Extraer de Neo4j y hacer JOIN)
    # Nota: Activamos el entorno virtual (venv) antes de ejecutar el script
    build_features = BashOperator(
        task_id='extract_and_build_features',
        bash_command='cd ~/fraud-detection-system && source venv/bin/activate && python src/features/create_master_table.py',
    )

    # 4. Tarea B: Reentrenar el Modelo y Registrar en MLflow
    train_model = BashOperator(
        task_id='train_xgboost_model',
        bash_command='cd ~/fraud-detection-system && source venv/bin/activate && python src/models/train_model.py',
    )

    # 5. La Topología de Ejecución (Las Flechas del Grafo)
    # Esto significa: "build_features" va estrictamente antes de "train_model"
    build_features >> train_model
