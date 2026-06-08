from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ServiceRecordBase(BaseModel):
    vehicle_id: int
    description: str
    cost: float

class ServiceRecordCreate(ServiceRecordBase):
    pass

class ServiceRecord(ServiceRecordBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True
