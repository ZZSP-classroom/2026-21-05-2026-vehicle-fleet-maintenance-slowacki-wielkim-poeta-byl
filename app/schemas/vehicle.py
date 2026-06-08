from pydantic import BaseModel
from typing import Optional
from app.models.vehicle import VehicleStatus

class VehicleBase(BaseModel):
    vin: str
    make: str
    model: str
    year: int
    engine_type: Optional[str] = None
    status: Optional[VehicleStatus] = VehicleStatus.ACTIVE

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int

    class Config:
        from_attributes = True
