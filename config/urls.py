""" All modules urls define here."""
from fastapi import APIRouter
from event_management.views import event_router

url_route = APIRouter()

# event module
url_route.include_router(event_router, prefix="/events")