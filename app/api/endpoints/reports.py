import os
import pandas as pd
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.api.dependencies import get_db
from app.models.vehicle import Vehicle
from app.models.maintenance import ServiceRecord

router = APIRouter()

def cleanup_file(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)

@router.get("/maintenance-costs")
async def get_maintenance_costs_report(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Vehicle).options(selectinload(Vehicle.service_records)))
    vehicles = result.scalars().all()
    
    data = []
    for v in vehicles:
        for record in v.service_records:
            data.append({
                "make": v.make,
                "model": v.model,
                "cost": float(record.cost)
            })
            
    if data:
        df = pd.DataFrame(data)
        # Group by make and model
        summary_df = df.groupby(["make", "model"])["cost"].sum().reset_index()
    else:
        summary_df = pd.DataFrame(columns=["make", "model", "cost"])
        
    filepath = "maintenance_costs_report.csv"
    summary_df.to_csv(filepath, index=False)
    
    background_tasks.add_task(cleanup_file, filepath)
    
    return FileResponse(filepath, media_type="text/csv", filename="maintenance_costs_report.csv")
