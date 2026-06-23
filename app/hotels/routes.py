from fastapi import APIRouter, Depends # Importamos APIRouter para crear rutas modulares y Depends para inyectar dependencias
from sqlalchemy.orm import Session # Importamos Session para tipar la sesión de base de datos
from typing import List, Optional # Importamos List y Optional para tipar las respuestas y parámetros opcionales
from app.database import get_db # Importamos la función get_db para obtener una sesión de base de datos
from app.errors import ResourceNotFoundException, DuplicateHotelException, BadRequestException # Importamos excepciones específicas
from .models import Hotel # Importamos el modelo Hotel para interactuar con la tabla de hoteles en la base de datos
from .schemas import HotelCreate, HotelUpdate, HotelResponse # Importamos los esquemas de Pydantic para validar y serializar los datos de entrada y salida de los endpoints

router = APIRouter(prefix="/hotels", tags=["Hotels"]) 
# Creamos un router para las rutas relacionadas con hoteles, con un prefijo común y etiquetas para la documentación automática

# --- FUNCIONES AUXILIARES (DRY) ---
def _get_hotel_by_id(db: Session, hotel_id: int) -> Hotel:
    """Obtiene un hotel por ID, lanza excepción si no existe"""
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise ResourceNotFoundException(f"Hotel with ID {hotel_id} not found")
    return hotel

def _validate_hotel_name_available(db: Session, name: str, exclude_id: Optional[int] = None) -> None:
    """Valida que el nombre del hotel no esté registrado (excluyendo un ID si es necesario)"""
    query = db.query(Hotel).filter(Hotel.name == name.strip())
    if exclude_id:
        query = query.filter(Hotel.id != exclude_id)
    if query.first():
        raise DuplicateHotelException(f"Hotel name '{name}' is already registered")

def _validate_input_strings(name: str, city: str) -> None:
    """Valida que los strings de entrada no sean vacíos"""
    if not name or not name.strip():
        raise BadRequestException("Hotel name cannot be empty")
    if not city or not city.strip():
        raise BadRequestException("Hotel city cannot be empty")

# --- ENDPOINTS CRUD ---

@router.post("/", response_model=HotelResponse, status_code=201)
def create_hotel(hotel_in: HotelCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo hotel.
    - Retorna **201 Created** (RESTful)
    - Valida nombre único y campos no vacíos
    """
    _validate_input_strings(hotel_in.name, hotel_in.city)
    _validate_hotel_name_available(db, hotel_in.name)
    
    new_hotel = Hotel(name=hotel_in.name.strip(), city=hotel_in.city.strip())
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel

@router.get("/", response_model=List[HotelResponse])
def list_hotels(city: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Listar todos los hoteles.
    - Query param `city` filtra por ciudad (case-insensitive)
    - Retorna **200 OK**
    """
    query = db.query(Hotel)
    if city and city.strip():
        query = query.filter(Hotel.city.ilike(f"%{city.strip()}%"))
    return query.all()

@router.get("/{hotel_id}", response_model=HotelResponse)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """
    Obtener un hotel específico por ID.
    - Retorna **200 OK** o **404 Not Found**
    """
    return _get_hotel_by_id(db, hotel_id)

@router.put("/{hotel_id}", response_model=HotelResponse)
def update_hotel(hotel_id: int, hotel_in: HotelCreate, db: Session = Depends(get_db)):
    """
    Actualizar completamente un hotel (requiere todos los campos).
    - Retorna **200 OK** o **404 Not Found**
    - Valida nombre único
    """
    _validate_input_strings(hotel_in.name, hotel_in.city)
    db_hotel = _get_hotel_by_id(db, hotel_id)
    
    if hotel_in.name.strip() != db_hotel.name:
        _validate_hotel_name_available(db, hotel_in.name, exclude_id=hotel_id)
    
    db_hotel.name = hotel_in.name.strip()
    db_hotel.city = hotel_in.city.strip()
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

@router.patch("/{hotel_id}", response_model=HotelResponse)
def partial_update_hotel(hotel_id: int, hotel_in: HotelUpdate, db: Session = Depends(get_db)):
    """
    Actualizar parcialmente un hotel (solo campos proporcionados).
    - Retorna **200 OK** o **404 Not Found**
    """
    db_hotel = _get_hotel_by_id(db, hotel_id)
    
    if hotel_in.name is not None:
        name = hotel_in.name.strip()
        if not name:
            raise BadRequestException("Hotel name cannot be empty")
        if name != db_hotel.name:
            _validate_hotel_name_available(db, name, exclude_id=hotel_id)
        db_hotel.name = name
    
    if hotel_in.city is not None:
        city = hotel_in.city.strip()
        if not city:
            raise BadRequestException("Hotel city cannot be empty")
        db_hotel.city = city
    
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

@router.delete("/{hotel_id}", status_code=204)
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un hotel por ID.
    - Retorna **204 No Content** o **404 Not Found**
    """
    db_hotel = _get_hotel_by_id(db, hotel_id)
    db.delete(db_hotel)
    db.commit()