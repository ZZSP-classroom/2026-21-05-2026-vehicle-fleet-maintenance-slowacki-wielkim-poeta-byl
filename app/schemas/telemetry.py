from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class TelemetryDataBase(BaseModel):
    vehicle_id: int
    speed: float = Field(..., ge=0, description="Speed must be non-negative")
    engine_rpm: float = Field(..., ge=0)
    coolant_temp: float = Field(..., le=300, description="Engine temperature cannot exceed 300°C")

class TelemetryDataCreate(TelemetryDataBase):
    pass

class TelemetryData(TelemetryDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
