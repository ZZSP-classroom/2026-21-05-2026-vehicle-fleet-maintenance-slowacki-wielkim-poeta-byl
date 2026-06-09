from pydantic import BaseModel
from typing import Optional, List
from app.schemas.vehicle import Vehicle

class PartBase(BaseModel):
    part_number: str
    name: str
    stock_quantity: int = 0
    supplier: Optional[str] = None

class PartCreate(PartBase):
    compatible_vehicle_ids: Optional[List[int]] = []

class Part(PartBase):
    id: int
    compatible_vehicles: List[Vehicle] = []

    class Config:
        from_attributes = True
