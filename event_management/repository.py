from sqlalchemy.orm import Session
from sqlalchemy import update
from .models import models
from datetime import datetime


class EventRepo:
    """ All event repository functions define here... """
    def create(db: Session, name:str, description:str, start_time:str, end_time:str, location:str, max_attendees:int):
        """ This function is used to create the event and returns event id... """
        event = models.Event(name = name, description = description, start_time = start_time, 
                             end_time =end_time, location=location,  max_attendees = max_attendees,status = 'scheduled' )
        db.add(event)
        db.commit()
        db.refresh(event)
        db.close() # closing the session
        
        return event.event_id
    
    def update(db: Session, event_id:int, name:str, description:str, start_time:str, end_time:str, location:str, max_attendees:int):
        """ This function is used to update the event details and returns event id... """
        # Convert ISO format string to datetime object
        start_time_obj = datetime.fromisoformat(start_time.rstrip('Z'))
        end_time_obj = datetime.fromisoformat(end_time.rstrip('Z'))
        event = db.query(models.Event).filter(models.Event.event_id == event_id).update({models.Event.name:name, models.Event.description:description, models.Event.start_time:start_time_obj, models.Event.end_time:end_time_obj, models.Event.location:location,models.Event.max_attendees:max_attendees})
        db.commit()
        db.close() # closing the session

        return event
    
class AttendeeRepo:

    def register_attendee(db: Session, first_name:str, last_name:str, email:str, phone_number:str, event_id:int):
        """ This function is used to create the attendee and returns attendee id... """
        event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
        attendees_list = db.query(models.Attendee).filter(models.Attendee.event_id == event_id).count()
        if attendees_list < event.max_attendees:
            attendee = models.Attendee(first_name = first_name, last_name = last_name, email = email, phone_number = phone_number, event_id = event_id, check_in_status = False)
            db.add(attendee)
            db.commit()
            db.refresh(attendee)
            db.close() # closing the session
        
            return event_id