from fastapi import FastAPI
from routers import health, events, ai

app = FastAPI()

app.include_router(health.router)
app.include_router(events.router)
app.include_router(ai.router)