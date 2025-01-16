import uuid
from DB import Base
from sqlalchemy import Boolean, String, ForeignKey, Column, Integer, DateTime, Enum
from sqlalchemy.orm import relationship


BaseClass = Base

class Event(BaseClass):
    __tablename__ = "event"
    event_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    start_time = Column(DateTime)
    end_time =Column(DateTime)
    location=Column(String)
    max_attendees = Column(Integer)
    status = Column(Enum('scheduled', 'ongoing', 'completed', 'canceled', name='event_statuses'))
    attendee_rel = relationship("Attendee", back_populates= "event_key")

class Attendee(BaseClass):
    __tablename__ = "attendee"
    attendee_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String,unique=True)
    phone_number = Column(String)
    event_id = Column (Integer, ForeignKey('event.event_id'), nullable=False)
    check_in_status = Column(Boolean)
    event_key = relationship("Event", back_populates="attendee_rel")