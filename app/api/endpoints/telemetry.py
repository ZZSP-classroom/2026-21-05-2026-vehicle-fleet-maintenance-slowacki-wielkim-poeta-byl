from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.crud import telemetry as crud_telemetry
from app.schemas.telemetry import TelemetryData, TelemetryDataCreate
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=TelemetryData)
def create_telemetry_data(telemetry: TelemetryDataCreate, db: Session = Depends(get_db)):
    return crud_telemetry.create_telemetry_data(db=db, telemetry=telemetry)

@router.get("/vehicle/{vehicle_id}", response_model=List[TelemetryData])
def read_telemetry_data(vehicle_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_telemetry.get_telemetry_for_vehicle(db, vehicle_id=vehicle_id, skip=skip, limit=limit)
