import os 
# Para manejar variables de entorno
from sqlalchemy import create_engine 
# Para crear el motor de conexión a la base de datos
from sqlalchemy.orm import sessionmaker, declarative_base 
# sessionmaker para crear sesiones de base de datos, declarative_base para definir modelos
from dotenv import load_dotenv
# Cargar variables de entorno del archivo .env
load_dotenv()# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")# Asegúrate de que DATABASE_URL esté definida en tu archivo .env, por ejemplo:
# DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_base_de_datos
# Crear el motor de conexión para Postgres
engine = create_engine(DATABASE_URL)# Crear una clase de sesión local que se utilizará para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)# Crear las tablas en la base de datos (si no existen)
# Crear la clase base para los modelos de SQLAlchemy

# Clase base de la que heredarán todos los modelos de SQLAlchemy
Base = declarative_base()

# Dependencia para inyectar la sesión en los endpoints
def get_db(): # Esta función se puede usar como dependencia en FastAPI para obtener una sesión de base de datos
    db = SessionLocal() # Crear una nueva sesión de base de datos
    try:# Devolver la sesión para su uso en los endpoints
        yield db # La función yield permite que la sesión se use en el contexto de un endpoint y luego se cierre automáticamente después de su uso
    finally:# Asegurarse de cerrar la sesión después de su uso para liberar recursos
        db.close()# Cerrar la sesión de base de datos después de su uso