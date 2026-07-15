from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_code = Column(String, unique=True, nullable=False, index=True)
    guest_name = Column(String, nullable=False)
    guest_email = Column(String, nullable=False, index=True)
    check_in = Column(Date, nullable=False, index=True)
    check_out = Column(Date, nullable=False, index=True)
    total_price = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="confirmed", index=True)

    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)

    room = relationship("Room", back_populates="bookings")
