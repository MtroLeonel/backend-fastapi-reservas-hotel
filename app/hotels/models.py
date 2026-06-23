from sqlalchemy import Column, Integer, String # Importar tipos de datos para definir columnas en la base de datos
from app.database import Base # Importar la clase base para los modelos de SQLAlchemy

class Hotel(Base): # Definir el modelo de datos para un hotel, que se mapeará a una tabla en la base de datos
    __tablename__ = "hotels"# Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True) # Columna de ID, que es la clave primaria y se indexa para mejorar el rendimiento de las consultas
    name = Column(String, unique=True, index=True)# Columna de nombre del hotel, que debe ser única y se indexa para mejorar el rendimiento de las consultas
    city = Column(String, index=True)# Columna de ciudad donde se encuentra el hotel, que se indexa para mejorar el rendimiento de las consultas

    # Relación con la tabla de habitaciones (si es necesario)
