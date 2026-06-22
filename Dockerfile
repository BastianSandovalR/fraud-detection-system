# 1. Imagen Base: Usamos un Linux oficial de Python, versión ligera (slim)
FROM python:3.11-slim

# 2. Directorio de Trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar archivos de dependencias e instalarlas
# (Nota: Asumimos que generarás un requirements.txt, pero por ahora lo instalamos directo)
# 3. Copiar archivos de dependencias e instalarlas con un timeout extendido
RUN pip install --default-timeout=1000 --no-cache-dir fastapi uvicorn pydantic pandas xgboost-cpu

# 4. Copiar el código fuente y los modelos a la caja
# Copiamos la carpeta src completa
COPY ./src /app/src

# IMPORTANTE: En un entorno real, descargaríamos el modelo de MLflow aquí.
# Para este laboratorio, si tuvieras el .pkl, lo copiaríamos también.

# 5. Exponer el puerto por donde escuchará la API
EXPOSE 8000

# 6. El comando de encendido automático
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
