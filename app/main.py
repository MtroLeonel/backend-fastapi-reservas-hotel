# importamos FastAPI para crear la aplicación web
from fastapi import FastAPI
# Creamos una instancia de FastAPI
app = FastAPI()
# Definimos una ruta para la raíz del sitio web
@app.get("/")
# La función home se ejecutará cuando se acceda a la ruta "/"
def home():
    # Devolvemos un mensaje de éxito en formato JSON
    return {"status": "¡FastAPI corriendo en Docker exitosamente!"}