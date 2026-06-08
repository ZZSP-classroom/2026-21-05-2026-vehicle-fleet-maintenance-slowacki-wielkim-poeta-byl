from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class TelemetryData(Base):
    __tablename__ = "telemetry_data"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    speed = Column(Float)
    engine_rpm = Column(Float)
    coolant_temp = Column(Float)
    
    vehicle = relationship("Vehicle", back_populates="telemetry_data")
