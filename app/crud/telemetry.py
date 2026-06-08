from sqlalchemy.orm import Session
from app.models.telemetry import TelemetryData
from app.schemas.telemetry import TelemetryDataCreate

def create_telemetry_data(db: Session, telemetry: TelemetryDataCreate):
    db_telemetry = TelemetryData(**telemetry.model_dump())
    db.add(db_telemetry)
    db.commit()
    db.refresh(db_telemetry)
    return db_telemetry

def get_telemetry_for_vehicle(db: Session, vehicle_id: int, skip: int = 0, limit: int = 100):
    return db.query(TelemetryData).filter(TelemetryData.vehicle_id == vehicle_id).offset(skip).limit(limit).all()
