import pandas as pd
import numpy as np
# Importaciones modernas desde la raíz y presets
from evidently import Report
from evidently.presets import DataDriftPreset

print("🕵️ Iniciando simulación de comportamiento criminal...")

# 1. LOS DATOS DE ENTRENAMIENTO (Reference Data)
np.random.seed(42)
reference_data = pd.DataFrame({
    "amount": np.random.normal(loc=500, scale=100, size=1000),
    "pagerank_score": np.random.normal(loc=0.8, scale=0.1, size=1000)
})

# 2. LOS DATOS NUEVOS EN PRODUCCIÓN (Current Data)
current_data = pd.DataFrame({
    "amount": np.random.normal(loc=15, scale=5, size=1000),
    "pagerank_score": np.random.normal(loc=0.8, scale=0.1, size=1000)
})

print("📊 Evaluando datos...")

# 3. El "Report" ahora es solo una plantilla de configuración
report_config = Report(metrics=[DataDriftPreset()])

# 4. Al hacer .run(), devuelve un NUEVO objeto con la evaluación real
my_eval = report_config.run(reference_data=reference_data, current_data=current_data)

# 5. Guardamos el objeto resultante (my_eval), NO la plantilla
report_path = "drift_report.html"
my_eval.save_html(report_path)

print(f"✅ ¡Autopsia de datos completada! Reporte guardado en: {report_path}")
