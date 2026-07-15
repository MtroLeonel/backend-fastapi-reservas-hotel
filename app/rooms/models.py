
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False, index=True)
    room_type = Column(String, nullable=False, index=True)
    capacity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)

    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False, index=True)

    hotel = relationship("Hotel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room", cascade="all, delete-orphan")