import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.errors import HotelAPIException
from app.hotels.routes import router as hotels_router

load_dotenv()


def _get_bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


app_env = os.getenv("APP_ENV", "development").strip().lower()
app_title = os.getenv("APP_TITLE", "Enterprise Hotel API")
debug_mode = _get_bool_env("DEBUG", default=app_env == "development")
enable_docs = _get_bool_env("ENABLE_DOCS", default=app_env != "production")

docs_url = "/docs" if enable_docs else None
redoc_url = "/redoc" if enable_docs else None
openapi_url = "/openapi.json" if enable_docs else None

# Creamos una instancia de FastAPI
app = FastAPI(
    title=app_title,
    debug=debug_mode,
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
)

# --- MANEJADOR DE EXCEPCIONES GLOBAL ---
# Cada vez que nuestro código lance un 'HotelAPIException', este bloque lo captura
@app.exception_handler(HotelAPIException) # Decorador para registrar un manejador de excepciones específico para HotelAPIException
def hotel_exception_handler(request: Request, exc: HotelAPIException): # Función que se ejecuta cuando se captura una HotelAPIException, recibe el objeto de la solicitud y la excepción capturada
    return JSONResponse(
        status_code=exc.status_code, # Usamos el código de estado definido en la excepción personalizada
        content={"success": False, "error": exc.message} # Devolvemos una respuesta JSON con un formato consistente para errores, incluyendo el mensaje de error definido en la excepción personalizada
    )

# Añadimos el router de hoteles a la aplicación
app.include_router(hotels_router, prefix="/api/v1") # Registramos el router de hoteles con un prefijo común para todas las rutas relacionadas con hoteles, lo que ayuda a organizar la API y mantener una estructura clara

# Definimos una ruta para la raíz del sitio web
@app.get("/")
# La función home se ejecutará cuando se acceda a la ruta "/"
def home():
    # Devolvemos un mensaje de éxito en formato JSON
    return {"status": "¡FastAPI corriendo en Docker exitosamente!"}
