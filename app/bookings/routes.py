from datetime import date, datetime
import secrets
import string
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import BadRequestException, ResourceNotFoundException
from app.rooms.models import Room
from .models import Booking
from .schemas import BookingCreate, BookingResponse, BookingUpdate

router = APIRouter(prefix="/bookings", tags=["Bookings"])

ALLOWED_BOOKING_STATUSES = {
    "confirmed",
    "checked_in",
    "checked_out",
    "cancelled",
    "no_show",
}


def _get_booking_by_id(db: Session, booking_id: int) -> Booking:
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise ResourceNotFoundException(f"Booking with ID {booking_id} not found")
    return booking


def _get_room_by_id(db: Session, room_id: int) -> Room:
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise ResourceNotFoundException(f"Room with ID {room_id} not found")
    return room


def _generate_booking_code() -> str:
    date_part = datetime.utcnow().strftime("%Y%m%d")
    token = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return f"RSV-{date_part}-{token}"


def _create_unique_booking_code(db: Session, max_attempts: int = 5) -> str:
    for _ in range(max_attempts):
        code = _generate_booking_code()
        exists = db.query(Booking).filter(Booking.booking_code == code).first()
        if not exists:
            return code
    raise BadRequestException("Could not generate a unique booking code")


def _validate_booking_fields(
    guest_name: str,
    guest_email: str,
    check_in: date,
    check_out: date,
    status: str,
) -> None:
    if not guest_name or not guest_name.strip():
        raise BadRequestException("Guest name cannot be empty")
    if not guest_email or not guest_email.strip() or "@" not in guest_email:
        raise BadRequestException("Guest email is invalid")
    if check_out <= check_in:
        raise BadRequestException("Check-out date must be later than check-in date")
    if not status or not status.strip():
        raise BadRequestException("Booking status cannot be empty")

    normalized_status = status.strip().lower()
    if normalized_status not in ALLOWED_BOOKING_STATUSES:
        raise BadRequestException(
            "Invalid booking status. Allowed values: confirmed, checked_in, checked_out, cancelled, no_show"
        )


def _calculate_total_price(check_in: date, check_out: date, room_price: int) -> int:
    nights = (check_out - check_in).days
    if nights <= 0:
        raise BadRequestException("Booking must include at least one night")
    return nights * room_price


def _validate_booking_overlap(
    db: Session,
    room_id: int,
    check_in: date,
    check_out: date,
    exclude_booking_id: Optional[int] = None,
) -> None:
    query = db.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.status != "cancelled",
        Booking.check_in < check_out,
        Booking.check_out > check_in,
    )

    if exclude_booking_id is not None:
        query = query.filter(Booking.id != exclude_booking_id)

    if query.first():
        raise BadRequestException("This room already has an active booking for the selected dates")


@router.post("/", response_model=BookingResponse, status_code=201)
def create_booking(booking_in: BookingCreate, db: Session = Depends(get_db)):
    _validate_booking_fields(
        booking_in.guest_name,
        booking_in.guest_email,
        booking_in.check_in,
        booking_in.check_out,
        booking_in.status,
    )
    room = _get_room_by_id(db, booking_in.room_id)

    if booking_in.status.strip().lower() != "cancelled":
        _validate_booking_overlap(
            db,
            booking_in.room_id,
            booking_in.check_in,
            booking_in.check_out,
        )

    total_price = _calculate_total_price(
        booking_in.check_in,
        booking_in.check_out,
        room.price,
    )

    new_booking = Booking(
        booking_code=_create_unique_booking_code(db),
        room_id=booking_in.room_id,
        guest_name=booking_in.guest_name.strip(),
        guest_email=booking_in.guest_email.strip().lower(),
        check_in=booking_in.check_in,
        check_out=booking_in.check_out,
        total_price=total_price,
        status=booking_in.status.strip().lower(),
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


@router.get("/", response_model=List[BookingResponse])
def list_bookings(
    room_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Booking)

    if room_id is not None:
        query = query.filter(Booking.room_id == room_id)

    if status and status.strip():
        query = query.filter(Booking.status == status.strip().lower())

    return query.all()


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    return _get_booking_by_id(db, booking_id)


@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: int, booking_in: BookingCreate, db: Session = Depends(get_db)):
    db_booking = _get_booking_by_id(db, booking_id)

    _validate_booking_fields(
        booking_in.guest_name,
        booking_in.guest_email,
        booking_in.check_in,
        booking_in.check_out,
        booking_in.status,
    )
    room = _get_room_by_id(db, booking_in.room_id)

    if booking_in.status.strip().lower() != "cancelled":
        _validate_booking_overlap(
            db,
            booking_in.room_id,
            booking_in.check_in,
            booking_in.check_out,
            exclude_booking_id=booking_id,
        )

    total_price = _calculate_total_price(
        booking_in.check_in,
        booking_in.check_out,
        room.price,
    )

    db_booking.room_id = booking_in.room_id
    db_booking.guest_name = booking_in.guest_name.strip()
    db_booking.guest_email = booking_in.guest_email.strip().lower()
    db_booking.check_in = booking_in.check_in
    db_booking.check_out = booking_in.check_out
    db_booking.total_price = total_price
    db_booking.status = booking_in.status.strip().lower()

    db.commit()
    db.refresh(db_booking)
    return db_booking


@router.patch("/{booking_id}", response_model=BookingResponse)
def partial_update_booking(booking_id: int, booking_in: BookingUpdate, db: Session = Depends(get_db)):
    db_booking = _get_booking_by_id(db, booking_id)

    next_room_id = booking_in.room_id if booking_in.room_id is not None else db_booking.room_id
    next_guest_name = booking_in.guest_name if booking_in.guest_name is not None else db_booking.guest_name
    next_guest_email = booking_in.guest_email if booking_in.guest_email is not None else db_booking.guest_email
    next_check_in = booking_in.check_in if booking_in.check_in is not None else db_booking.check_in
    next_check_out = booking_in.check_out if booking_in.check_out is not None else db_booking.check_out
    next_status = booking_in.status if booking_in.status is not None else db_booking.status

    if booking_in.room_id is not None:
        room = _get_room_by_id(db, booking_in.room_id)
    else:
        room = _get_room_by_id(db, db_booking.room_id)

    _validate_booking_fields(
        next_guest_name,
        next_guest_email,
        next_check_in,
        next_check_out,
        next_status,
    )

    if next_status.strip().lower() != "cancelled":
        _validate_booking_overlap(
            db,
            next_room_id,
            next_check_in,
            next_check_out,
            exclude_booking_id=booking_id,
        )

    total_price = _calculate_total_price(
        next_check_in,
        next_check_out,
        room.price,
    )

    db_booking.room_id = next_room_id
    db_booking.guest_name = next_guest_name.strip()
    db_booking.guest_email = next_guest_email.strip().lower()
    db_booking.check_in = next_check_in
    db_booking.check_out = next_check_out
    db_booking.total_price = total_price
    db_booking.status = next_status.strip().lower()

    db.commit()
    db.refresh(db_booking)
    return db_booking


@router.delete("/{booking_id}", status_code=204)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = _get_booking_by_id(db, booking_id)
    db.delete(db_booking)
    db.commit()
