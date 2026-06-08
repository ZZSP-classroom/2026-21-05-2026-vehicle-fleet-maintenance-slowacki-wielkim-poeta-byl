from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TelemetryDataBase(BaseModel):
    vehicle_id: int
    speed: float
    engine_rpm: float
    coolant_temp: float

class TelemetryDataCreate(TelemetryDataBase):
    pass

class TelemetryData(TelemetryDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
