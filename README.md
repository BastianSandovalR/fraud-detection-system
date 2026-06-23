# 🛡️ Fraud Detection System: End-to-End MLOps Architecture

He diseñado y orquestado un sistema MLOps end-to-end para detección de fraude en tiempo real, capaz de transformar transacciones tabulares aisladas en grafos de relaciones complejas mediante Neo4j. El sistema garantiza reproducibilidad total con DVC, observabilidad mediante Evidently AI y despliegue automatizado con pipelines de CI/CD, permitiendo una detección proactiva de anomalías incluso cuando los patrones de fraude evolucionan.

## 🏗️ Arquitectura del Sistema

![Diagrama de Arquitectura de MLOps]
## 🏗️ Arquitectura del Sistema

```mermaid
graph TD
    %% Definición de Estilos
    classDef git fill:#f34f29,stroke:#fff,stroke-width:2px,color:#fff;
    classDef data fill:#007acc,stroke:#fff,stroke-width:2px,color:#fff;
    classDef model fill:#2ea44f,stroke:#fff,stroke-width:2px,color:#fff;
    classDef deploy fill:#0db7ed,stroke:#fff,stroke-width:2px,color:#fff;

    subgraph "1. Data Pipeline (DVC & Airflow)"
        A[(Datos Transaccionales)] -->|DVC Pull| B[Limpieza & Transformación]
        B --> C[(Neo4j Graph DB)]
        C -->|PageRank Features| D[Ingeniería de Variables]
        D --> E[Entrenamiento XGBoost]
    end

    subgraph "2. Model Registry (Cloud)"
        E -->|Registra Métricas y .pkl| F[(DagsHub / MLflow)]
    end

    subgraph "3. CI/CD & Deploy (GitHub Actions)"
        G[Git Push Código]:::git --> H{Tests Flake8}
        H -->|Pasa| I[Construir Docker Image]
        I --> J[FastAPI Service]:::deploy
        F -.->|Descarga Modelo| J
    end

    subgraph "4. Monitoreo (Evidently AI)"
        J --> K[Predicciones en Vivo]
        K --> L{Detección de Data Drift}
        L -.->|Alerta de Reentrenamiento| A
    end

    %% Asignación de colores
    A:::data; B:::data; C:::data; D:::data; E:::model; F:::model; ```
El ciclo de vida del proyecto está dividido en dos flujos principales:
1. **Flujo de Datos (Data Pipeline):** Orquestado por Apache Airflow, extrae datos crudos, calcula topologías de red (PageRank) en Neo4j y reentrena modelos XGBoost rastreando artefactos en DagsHub (MLflow remoto).
2. **Flujo de Código (CI/CD):** Las modificaciones en el código disparan flujos de GitHub Actions que ejecutan pruebas de calidad (Flake8) y construyen imágenes Docker inmutables para el despliegue de la API (FastAPI).

## 🛠️ Stack Tecnológico

* **Orquestación & CI/CD:** Apache Airflow, GitHub Actions
* **Feature Engineering & Grafos:** Polars, Apache Spark, Neo4j
* **Modelado predictivo:** XGBoost
* **MLOps & Control de Versiones:** DVC (Data Version Control), MLflow (DagsHub)
* **Observabilidad:** Evidently AI
* **Despliegue:** FastAPI, Docker

## 🚀 Cómo reproducir este proyecto

Este proyecto está diseñado bajo el estándar de "Reproducibilidad Total". Para ejecutar este sistema localmente y descargar los datos exactos del entrenamiento original:

**1. Clonar el repositorio y configurar el entorno**
```bash
git clone [https://github.com/BastianSandovalR/fraud-detection-system.git](https://github.com/BastianSandovalR/fraud-detection-system.git)
cd fraud-detection-system
python -m venv venv
source venv/bin/activate  # En Linux/Mac
pip install -r requirements.txt
