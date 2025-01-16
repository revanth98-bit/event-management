from DB import session
from fastapi import APIRouter, Depends, status, responses, HTTPException
from .models.request_models import CreateEvent, UpdateEvent, RegisterAttendee, CheckInAttendee
from .models import models, response_models
from .repository import EventRepo, AttendeeRepo
from util import messages
from sqlalchemy import select
from datetime import datetime


event_router = APIRouter()
TAGS = ["Event_Management"]


@event_router.post("/create_event", tags=TAGS)
async def create_event(event:CreateEvent):
    """example of creating the event
            {
        "name": "event 2",
        "description": "event 2 for the event 1",
        "start_time": "2025-01-17T09:28:45.610",
        "end_time": "2025-01-17T12:28:45.610",
        "location": "Nellore",
        "max_attendees": 3
        }"""
    try:
        event =  EventRepo.create(session(),event.name, event.description, event.start_time, event.end_time, event.location, event.max_attendees)
        return response_models.CreateEventResponse(
            id=event,
            message= messages.SUCCESS['EVENT_CREATED_SUCCESSFULLY'],
            code = status.HTTP_200_OK
        )
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@event_router.put("/update_event", tags=TAGS)
async def update_event(event:UpdateEvent):
    try:
        event = EventRepo.update(session(),event.event_id,event.name, event.description, event.start_time, event.end_time, event.location, event.max_attendees)
        return response_models.UpdateEventResponse(
            id= event,
            message=messages.SUCCESS['EVENT_UPDATED_SUCCESSFULLY'],
            code=status.HTTP_200_OK)
    
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@event_router.get("/get_events/{status}/{location}/{date}", tags= TAGS)
async def get_event(status: str,location:str,date:datetime):
    event = session().query(models.Event).filter(models.Event.status== status, models.Event.location==location, models.Event.start_time==date).first()
    if not event:
        raise HTTPException(status_code=404, detail=messages.ERROR['EVENT_NOT_FOUND'])
    if event.end_time < datetime.now() and event.status != 'completed':
        event.status = 'completed'
        session().commit()
    return event


@event_router.get("/get_attendees/{event_id}", tags= TAGS)
async def get_attendees(event_id: int):
    attendees = session().query(models.Attendee).filter(models.Attendee.event_id == event_id).all()
    return attendees


@event_router.post("/register_attendee", tags=TAGS)
async def register_attendee(attendee:RegisterAttendee):
    try:

        event = session().query(models.Event).filter(models.Event.event_id == attendee.event_id).first()
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.ERROR['EVENT_NOT_FOUND'])
        attendees_list = session().query(models.Attendee).filter(models.Attendee.event_id == attendee.event_id).count()
         # Check if an attendee already exists
        attendee_exists = session().execute(
            select(session().query(models.Attendee)
                    .filter(models.Attendee.event_id == attendee.event_id,
                            models.Attendee.email == attendee.email)
                    .exists())
        ).scalar()

        if attendee_exists:
            return responses.JSONResponse(
                content={"message": messages.ERROR['ATTENDEE_ALREADY_REGISTERED'].format(event.name), "code": status.HTTP_400_BAD_REQUEST},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if attendees_list < event.max_attendees:
            attendee_id = AttendeeRepo.register_attendee(session(), attendee.first_name, attendee.last_name, attendee.email, attendee.phonenumber, attendee.event_id)
            return response_models.RegisterAttendeeResponse(
                id=attendee_id,
                message=messages.SUCCESS['REGISTRATION_SUCCESSFULL'].format(event.name),
                code=status.HTTP_200_OK
            )

        return responses.JSONResponse(
                    content={"message": messages.ERROR['ATTENDEE_LIMIT_REACHED'], "code": status.HTTP_400_BAD_REQUEST},
                    status_code=status.HTTP_400_BAD_REQUEST
                )

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

