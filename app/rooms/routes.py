from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.errors import ResourceNotFoundException, BadRequestException
from app.hotels.models import Hotel
from .models import Room
from .schemas import RoomCreate, RoomUpdate, RoomResponse

router = APIRouter(prefix="/rooms", tags=["Rooms"])


def _get_room_by_id(db: Session, room_id: int) -> Room:
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise ResourceNotFoundException(f"Room with ID {room_id} not found")
    return room


def _get_hotel_by_id(db: Session, hotel_id: int) -> Hotel:
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise ResourceNotFoundException(f"Hotel with ID {hotel_id} not found")
    return hotel


def _validate_room_fields(number: str, room_type: str, capacity: int, price: int) -> None:
    if not number or not number.strip():
        raise BadRequestException("Room number cannot be empty")
    if not room_type or not room_type.strip():
        raise BadRequestException("Room type cannot be empty")
    if capacity <= 0:
        raise BadRequestException("Room capacity must be greater than 0")
    if price < 0:
        raise BadRequestException("Room price cannot be negative")


@router.post("/", response_model=RoomResponse, status_code=201)
def create_room(room_in: RoomCreate, db: Session = Depends(get_db)):
    _validate_room_fields(
        room_in.number,
        room_in.room_type,
        room_in.capacity,
        room_in.price,
    )
    _get_hotel_by_id(db, room_in.hotel_id)

    existing_room = (
        db.query(Room)
        .filter(
            Room.hotel_id == room_in.hotel_id,
            Room.number == room_in.number.strip(),
        )
        .first()
    )
    if existing_room:
        raise BadRequestException(
            f"Room number '{room_in.number}' already exists for this hotel"
        )

    new_room = Room(
        number=room_in.number.strip(),
        room_type=room_in.room_type.strip(),
        capacity=room_in.capacity,
        price=room_in.price,
        is_available=room_in.is_available,
        hotel_id=room_in.hotel_id,
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


@router.get("/", response_model=List[RoomResponse])
def list_rooms(hotel_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Room)
    if hotel_id is not None:
        query = query.filter(Room.hotel_id == hotel_id)
    return query.all()


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    return _get_room_by_id(db, room_id)


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(room_id: int, room_in: RoomCreate, db: Session = Depends(get_db)):
    _validate_room_fields(
        room_in.number,
        room_in.room_type,
        room_in.capacity,
        room_in.price,
    )
    _get_hotel_by_id(db, room_in.hotel_id)

    db_room = _get_room_by_id(db, room_id)

    duplicate_room = (
        db.query(Room)
        .filter(
            Room.hotel_id == room_in.hotel_id,
            Room.number == room_in.number.strip(),
            Room.id != room_id,
        )
        .first()
    )
    if duplicate_room:
        raise BadRequestException(
            f"Room number '{room_in.number}' already exists for this hotel"
        )

    db_room.number = room_in.number.strip()
    db_room.room_type = room_in.room_type.strip()
    db_room.capacity = room_in.capacity
    db_room.price = room_in.price
    db_room.is_available = room_in.is_available
    db_room.hotel_id = room_in.hotel_id

    db.commit()
    db.refresh(db_room)
    return db_room


@router.patch("/{room_id}", response_model=RoomResponse)
def partial_update_room(room_id: int, room_in: RoomUpdate, db: Session = Depends(get_db)):
    db_room = _get_room_by_id(db, room_id)

    if room_in.hotel_id is not None:
        _get_hotel_by_id(db, room_in.hotel_id)

    if room_in.number is not None:
        number = room_in.number.strip()
        if not number:
            raise BadRequestException("Room number cannot be empty")

        target_hotel_id = room_in.hotel_id if room_in.hotel_id is not None else db_room.hotel_id
        duplicate_room = (
            db.query(Room)
            .filter(
                Room.hotel_id == target_hotel_id,
                Room.number == number,
                Room.id != room_id,
            )
            .first()
        )
        if duplicate_room:
            raise BadRequestException(
                f"Room number '{room_in.number}' already exists for this hotel"
            )
        db_room.number = number

    if room_in.room_type is not None:
        room_type = room_in.room_type.strip()
        if not room_type:
            raise BadRequestException("Room type cannot be empty")
        db_room.room_type = room_type

    if room_in.capacity is not None:
        if room_in.capacity <= 0:
            raise BadRequestException("Room capacity must be greater than 0")
        db_room.capacity = room_in.capacity

    if room_in.price is not None:
        if room_in.price < 0:
            raise BadRequestException("Room price cannot be negative")
        db_room.price = room_in.price

    if room_in.is_available is not None:
        db_room.is_available = room_in.is_available

    if room_in.hotel_id is not None:
        db_room.hotel_id = room_in.hotel_id

    db.commit()
    db.refresh(db_room)
    return db_room


@router.delete("/{room_id}", status_code=204)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = _get_room_by_id(db, room_id)
    db.delete(db_room)
    db.commit()