from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.dependencies import get_db
from app.schemas.telemetry import TelemetryData, TelemetryDataCreate
from app.models.telemetry import TelemetryData as TelemetryDataModel

router = APIRouter()

@router.post("/", status_code=201)
async def create_telemetry_batch(
    telemetry_records: List[TelemetryDataCreate], 
    db: AsyncSession = Depends(get_db)
):
    db_records = [TelemetryDataModel(**record.model_dump()) for record in telemetry_records]
    db.add_all(db_records)
    await db.commit()
    return {"message": f"Successfully ingested {len(db_records)} telemetry records"}
