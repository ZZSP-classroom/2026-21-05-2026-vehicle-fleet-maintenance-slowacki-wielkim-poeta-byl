from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

part_vehicle_compatibility = Table(
    "part_vehicle_compatibility",
    Base.metadata,
    Column("part_id", Integer, ForeignKey("parts.id"), primary_key=True),
    Column("vehicle_id", Integer, ForeignKey("vehicles.id"), primary_key=True)
)

class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    part_number = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    stock_quantity = Column(Integer, default=0)
    supplier = Column(String)
    
    compatible_vehicles = relationship("Vehicle", secondary=part_vehicle_compatibility, backref="compatible_parts")
