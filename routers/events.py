from fastapi import APIRouter, Query
from controllers.calendar import get_events, create_event, delete_event, update_event, get_free_time
from models.events import EventCreate, EventUpdate

router = APIRouter()

@router.get("/events")
def events():
    return get_events()

@router.post("/create-event")
def create(event: EventCreate):

    return create_event(
        event.summary,
        event.start,
        event.end
    )

@router.delete("/event/{event_id}")
def delete(event_id: str):
    return delete_event(event_id)

@router.put("/event/{event_id}")
def update(event_id: str, event: EventUpdate):
    return update_event(
        event_id,
        event.summary,
        event.start,
        event.end
    )

@router.get("/free-time")
def free_time(
    time_min: str = Query(..., description="Start time in ISO format (e.g. 2026-03-08T09:00:00+07:00)"),
    time_max: str = Query(..., description="End time in ISO format (e.g. 2026-03-08T17:00:00+07:00)")
):
    return get_free_time(time_min, time_max)