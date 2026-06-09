from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.crud import vehicle as crud_vehicle
from app.schemas.vehicle import Vehicle, VehicleCreate
from app.schemas.maintenance import ServiceRecord, ServiceRecordCreate
from app.models.vehicle import Vehicle as VehicleModel
from app.models.maintenance import ServiceRecord as ServiceRecordModel
from app.api.dependencies import get_db

router = APIRouter()

def calculate_next_due_date_task(vehicle_id: int):
    # Simulated email function
    print(f"SIMULATED EMAIL: Vehicle {vehicle_id} maintenance logged. Calculating next due date and checking mileage threshold.")

@router.post("/", response_model=Vehicle)
async def create_vehicle(vehicle: VehicleCreate, db: AsyncSession = Depends(get_db)):
    return await crud_vehicle.create_vehicle(db=db, vehicle=vehicle)

@router.get("/", response_model=List[Vehicle])
async def read_vehicles(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    vehicles = await crud_vehicle.get_vehicles(db, skip=skip, limit=limit)
    return vehicles

@router.get("/{vehicle_id}", response_model=Vehicle)
async def read_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    db_vehicle = await crud_vehicle.get_vehicle(db, vehicle_id=vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

@router.put("/{vehicle_id}", response_model=Vehicle)
async def update_vehicle(vehicle_id: int, vehicle: VehicleCreate, db: AsyncSession = Depends(get_db)):
    db_vehicle = await crud_vehicle.update_vehicle(db, vehicle_id=vehicle_id, vehicle_data=vehicle.model_dump())
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

@router.get("/{vehicle_id}/maintenance")
async def get_vehicle_maintenance(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(VehicleModel).options(selectinload(VehicleModel.service_records)).filter(VehicleModel.id == vehicle_id))
    db_vehicle = result.scalars().first()
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

@router.post("/{vehicle_id}/maintenance", response_model=ServiceRecord)
async def create_maintenance_record(
    vehicle_id: int, 
    record: ServiceRecordCreate, 
    background_tasks: BackgroundTasks, 
    db: AsyncSession = Depends(get_db)
):
    if record.vehicle_id != vehicle_id:
        raise HTTPException(status_code=400, detail="Vehicle ID mismatch")
    
    # Check if vehicle exists to ensure FK constraint conceptually or let DB throw IntegrityError. 
    # Let's do a quick check to return 404 cleanly.
    db_vehicle = await crud_vehicle.get_vehicle(db, vehicle_id=vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    db_record = ServiceRecordModel(**record.model_dump())
    db.add(db_record)
    await db.commit()
    await db.refresh(db_record)
    
    background_tasks.add_task(calculate_next_due_date_task, vehicle_id)
    
    return db_record
