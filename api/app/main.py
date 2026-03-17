import logging

from fastapi import FastAPI

from app.config import settings
from app.db import Base, engine
from app.routes.health import router as health_router
from app.routes.jobs import router as jobs_router


logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(
    title="Containerized Microservices API",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(health_router)
app.include_router(jobs_router)