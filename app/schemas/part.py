from pydantic import BaseModel
from typing import Optional

class PartBase(BaseModel):
    part_number: str
    name: str
    quantity: int
    supplier: Optional[str] = None
    compatible_makes: Optional[str] = None

class PartCreate(PartBase):
    pass

class Part(PartBase):
    id: int

    class Config:
        from_attributes = True
