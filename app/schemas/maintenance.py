from pydantic import BaseModel, condecimal
from datetime import datetime
from typing import Optional
from decimal import Decimal

class ServiceRecordBase(BaseModel):
    vehicle_id: int
    description: str
    cost: Decimal

class ServiceRecordCreate(ServiceRecordBase):
    pass

class ServiceRecord(ServiceRecordBase):
    id: int
    date_performed: datetime

    class Config:
        from_attributes = True
