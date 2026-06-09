from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.api.dependencies import get_db
from app.models.part import Part as PartModel
from app.models.vehicle import Vehicle as VehicleModel
from app.schemas.part import Part, PartCreate

router = APIRouter()

@router.post("/", response_model=Part)
async def create_part(part: PartCreate, db: AsyncSession = Depends(get_db)):
    part_data = part.model_dump(exclude={"compatible_vehicle_ids"})
    db_part = PartModel(**part_data)
    
    if part.compatible_vehicle_ids:
        vehicles_result = await db.execute(select(VehicleModel).filter(VehicleModel.id.in_(part.compatible_vehicle_ids)))
        vehicles = vehicles_result.scalars().all()
        db_part.compatible_vehicles = vehicles

    db.add(db_part)
    await db.commit()
    
    # Reload with relationships using selectinload to avoid greenlet error
    result = await db.execute(
        select(PartModel)
        .options(selectinload(PartModel.compatible_vehicles))
        .filter(PartModel.id == db_part.id)
    )
    db_part = result.scalars().first()
    return db_part

@router.get("/", response_model=List[Part])
async def read_parts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PartModel).options(selectinload(PartModel.compatible_vehicles)).offset(skip).limit(limit))
    return result.scalars().all()

@router.patch("/{part_id}/reduce-stock", response_model=Part)
async def reduce_stock(part_id: int, quantity: int, db: AsyncSession = Depends(get_db)):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity to reduce must be greater than 0")
        
    result = await db.execute(select(PartModel).options(selectinload(PartModel.compatible_vehicles)).filter(PartModel.id == part_id))
    part = result.scalars().first()
    
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
        
    if part.stock_quantity - quantity < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Stock quantity cannot be less than 0")
        
    part.stock_quantity -= quantity
    await db.commit()
    
    # Reload with relationships
    result = await db.execute(select(PartModel).options(selectinload(PartModel.compatible_vehicles)).filter(PartModel.id == part_id))
    part = result.scalars().first()
    return part
