from pydantic import BaseModel # Importar BaseModel de Pydantic para definir los esquemas de datos
from typing import Optional # Importar Optional para campos opcionales

class HotelBase(BaseModel): # Esquema base para los hoteles, que incluye los campos comunes
    name: str
    city: str

class HotelCreate(HotelBase): # Esquema para crear un hotel, que hereda de HotelBase y no agrega campos adicionales
    pass # No se necesitan campos adicionales para la creación, ya que HotelBase ya los define

class HotelUpdate(BaseModel): # Esquema para actualizar un hotel con campos opcionales
    name: Optional[str] = None
    city: Optional[str] = None

class HotelResponse(HotelBase): # Esquema para responder con información de un hotel, que hereda de HotelBase y agrega el campo ID
    id: int

    class Config: # Configuración adicional para el modelo de respuesta, indicando que se puede crear a partir de atributos (útil para SQLAlchemy)
        from_attributes = True # Permite que Pydantic cree instancias de HotelResponse a partir de objetos que tengan atributos correspondientes (como los modelos de SQLAlchemy)