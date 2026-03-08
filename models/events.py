from pydantic import BaseModel
from typing import Optional

class Event(BaseModel):
    title: str
    time: str

class EventCreate(BaseModel):
    summary: str
    start: str
    end: str

class EventUpdate(BaseModel):
    summary: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None