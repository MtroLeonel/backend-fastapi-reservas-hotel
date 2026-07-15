from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel


BookingStatus = Literal[
    "confirmed",
    "checked_in",
    "checked_out",
    "cancelled",
    "no_show",
]


class BookingBase(BaseModel):
    room_id: int
    guest_name: str
    guest_email: str
    check_in: date
    check_out: date
    status: BookingStatus = "confirmed"


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    room_id: Optional[int] = None
    guest_name: Optional[str] = None
    guest_email: Optional[str] = None
    check_in: Optional[date] = None
    check_out: Optional[date] = None
    status: Optional[BookingStatus] = None


class BookingResponse(BookingBase):
    id: int
    booking_code: str
    total_price: int

    class Config:
        from_attributes = True
