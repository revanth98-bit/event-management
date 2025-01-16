""" we define all the request models of user module here... """
from pydantic import BaseModel, EmailStr, constr, validator
from datetime import datetime
from typing import Optional
from dateutil.parser import parse
from sqlalchemy import select

from .models import Attendee
from DB import session



class CreateEvent(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    description: constr(strip_whitespace=True, min_length=1)
    start_time: datetime
    end_time: datetime
    location: constr(strip_whitespace=True, min_length=1)
    max_attendees: int

    @validator('end_time')
    def check_end_after_start(cls, v, values, **kwargs):
        if 'start_time' in values:
            # Ensure both start_time and end_time are datetime objects
            start_time = parse(values['start_time']) if isinstance(values['start_time'], str) else values['start_time']
            end_time = parse(v) if isinstance(v, str) else v
            if end_time <= start_time:
                raise ValueError('end_time must be after start_time')
        return v

    @validator('start_time', 'end_time', pre=True)
    def check_datetime_not_past(cls, v):
        # Parse if v is a string, otherwise use it directly
        event_time = parse(v) if isinstance(v, str) else v
        if event_time < datetime.now():
            raise ValueError('Date and time must be in the future')
        return v


class UpdateEvent(BaseModel):
    event_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    max_attendees: Optional[int] = None

    @validator('end_time')
    def check_end_after_start(cls, v, values, **kwargs):
        if 'start_time' in values:
            # Ensure both start_time and end_time are datetime objects
            start_time = parse(values['start_time']) if isinstance(values['start_time'], str) else values['start_time']
            end_time = parse(v) if isinstance(v, str) else v
            if end_time <= start_time:
                raise ValueError('end_time must be after start_time')
        return v

    @validator('start_time', 'end_time', pre=True)
    def check_datetime_not_past(cls, v):
        # Parse if v is a string, otherwise use it directly
        event_time = parse(v) if isinstance(v, str) else v
        if event_time < datetime.now():
            raise ValueError('Date and time must be in the future')
        return v


class RegisterAttendee(BaseModel):
    event_id: int
    first_name: constr(strip_whitespace=True, min_length=1)
    last_name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr
    phonenumber: constr(strip_whitespace=True, min_length=10, max_length=15)

    # Custom validator example
    @validator('phonenumber')
    def validate_phone_number(cls, v):
        if not v.isdigit():
            raise ValueError("Phone number must contain only digits")
        return v
    
class CheckInAttendee(BaseModel):
    event_id:int
    attendee_id:int

    @validator("event_id", "attendee_id")
    def validate_attende(cls, v):
        print(f"==>> v: {v}")
        attendee_exists = session().execute(
            select(session().query(Attendee)
                    .filter(Attendee.event_id == event_id,
                            Attendee.attendee_id == attendee_id)
                    .exists())
        ).scalar()
