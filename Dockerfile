# 1. Descarga una imagen oficial de Python ligera
FROM python:3.11-slim

# 2. Crea una carpeta interna en el contenedor para el código
WORKDIR /code

# 3. Copia el archivo de requerimientos hacia el contenedor
COPY ./requirements.txt /code/requirements.txt

# 4. Instala las librerías dentro del contenedor
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copia tu carpeta 'app' local dentro del contenedor
COPY ./app /code/app

# 6. Ejecuta FastAPI usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]