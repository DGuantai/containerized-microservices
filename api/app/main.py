import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.db import Base, engine
from app.routes.health import router as health_router
from app.routes.jobs import router as jobs_router


logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP LOGIC
    if os.getenv("SKIP_DB_INIT", "false").lower() != "true":
        Base.metadata.create_all(bind=engine)

    yield  # <-- app runs here

    # SHUTDOWN LOGIC (optional)
    # e.g., close connections, cleanup resources


app = FastAPI(
    title="Containerized Microservices API",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(health_router)
app.include_router(jobs_router)