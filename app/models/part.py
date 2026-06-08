from sqlalchemy import Column, Integer, String, Float
from app.db.base_class import Base

class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    part_number = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    supplier = Column(String)
    compatible_makes = Column(String) # Simple comma-separated for now
