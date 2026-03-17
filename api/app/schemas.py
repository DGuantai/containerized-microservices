from datetime import datetime

from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    payload: str = Field(..., min_length=1, max_length=5000)


class JobResponse(BaseModel):
    id: str
    payload: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class HealthResponse(BaseModel):
    status: str


class ReadinessResponse(BaseModel):
    app: str
    database: str
    redis: str