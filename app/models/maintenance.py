from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class ServiceRecord(Base):
    __tablename__ = "service_records"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    
    vehicle = relationship("Vehicle", back_populates="service_records")
