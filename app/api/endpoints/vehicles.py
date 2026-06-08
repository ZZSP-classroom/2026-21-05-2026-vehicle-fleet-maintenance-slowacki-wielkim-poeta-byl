from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import vehicle as crud_vehicle
from app.schemas.vehicle import Vehicle, VehicleCreate
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Vehicle)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    return crud_vehicle.create_vehicle(db=db, vehicle=vehicle)

@router.get("/", response_model=List[Vehicle])
def read_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vehicles = crud_vehicle.get_vehicles(db, skip=skip, limit=limit)
    return vehicles

@router.get("/{vehicle_id}", response_model=Vehicle)
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = crud_vehicle.get_vehicle(db, vehicle_id=vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle
