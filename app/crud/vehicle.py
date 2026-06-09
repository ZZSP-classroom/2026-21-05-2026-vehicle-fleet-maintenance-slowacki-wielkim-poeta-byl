from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate

async def get_vehicle(db: AsyncSession, vehicle_id: int):
    result = await db.execute(select(Vehicle).filter(Vehicle.id == vehicle_id))
    return result.scalars().first()

async def get_vehicles(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Vehicle).offset(skip).limit(limit))
    return result.scalars().all()

async def create_vehicle(db: AsyncSession, vehicle: VehicleCreate):
    db_vehicle = Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    await db.commit()
    await db.refresh(db_vehicle)
    return db_vehicle

async def update_vehicle(db: AsyncSession, vehicle_id: int, vehicle_data: dict):
    db_vehicle = await get_vehicle(db, vehicle_id)
    if db_vehicle:
        for key, value in vehicle_data.items():
            setattr(db_vehicle, key, value)
        await db.commit()
        await db.refresh(db_vehicle)
    return db_vehicle

async def delete_vehicle(db: AsyncSession, vehicle_id: int):
    db_vehicle = await get_vehicle(db, vehicle_id)
    if db_vehicle:
        await db.delete(db_vehicle)
        await db.commit()
    return db_vehicle
