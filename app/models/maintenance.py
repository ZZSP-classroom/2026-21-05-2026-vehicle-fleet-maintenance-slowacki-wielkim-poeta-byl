from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class ServiceRecord(Base):
    __tablename__ = "service_records"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    # Changed back to 'date' to align with the database schema structure
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String, nullable=False)
    cost = Column(Numeric(10, 2), nullable=False)
    
    vehicle = relationship("Vehicle", back_populates="service_records")