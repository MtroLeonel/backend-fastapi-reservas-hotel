from pydantic import BaseModel
from typing import Optional


class RoomBase(BaseModel):
    number: str
    room_type: str
    capacity: int
    price: int
    is_available: bool = True
    hotel_id: int


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    number: Optional[str] = None
    room_type: Optional[str] = None
    capacity: Optional[int] = None
    price: Optional[int] = None
    is_available: Optional[bool] = None
    hotel_id: Optional[int] = None


class RoomResponse(RoomBase):
    id: int

    class Config:
        from_attributes = True