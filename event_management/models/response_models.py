from pydantic import BaseModel
from typing import Optional

class CreateEventResponse(BaseModel):
    id: Optional[int] = None
    message: str
    code: int

    class Config:
        orm_mode = True

class UpdateEventResponse(BaseModel):
    id: Optional[int] = None
    message: str
    code: int

    class Config:
        orm_mode = True

class RegisterAttendeeResponse(BaseModel):
    id: Optional[int] = None
    message: str
    code: int

    class Config:
        orm_mode = True

class CheckInAttendeeResponse(BaseModel):
    message: str
    code: int

    class Config:
        orm_mode = True