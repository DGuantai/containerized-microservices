from fastapi import APIRouter
from sqlalchemy import text

from app.db import SessionLocal
from app.queue import get_redis_client
from app.schemas import HealthResponse, ReadinessResponse


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok")


@router.get("/ready", response_model=ReadinessResponse)
def readiness_check():
    database_status = "ok"
    redis_status = "ok"

    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
    except Exception:
        database_status = "error"

    try:
        redis_client = get_redis_client()
        redis_client.ping()
    except Exception:
        redis_status = "error"

    app_status = "ok" if database_status == "ok" and redis_status == "ok" else "degraded"

    return ReadinessResponse(
        app=app_status,
        database=database_status,
        redis=redis_status,
    )