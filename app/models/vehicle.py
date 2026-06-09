from sqlalchemy import Column, Integer, String, Float, Enum, Boolean
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base

class VehicleStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    IN_SHOP = "IN_SHOP"
    DECOMMISSIONED = "DECOMMISSIONED"

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String, unique=True, index=True, nullable=False)
    make = Column(String, index=True, nullable=False)
    model = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=False)
    engine_type = Column(String)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.ACTIVE)
    
    # Relationships
    service_records = relationship("ServiceRecord", back_populates="vehicle")
    telemetry_data = relationship("TelemetryData", back_populates="vehicle")
