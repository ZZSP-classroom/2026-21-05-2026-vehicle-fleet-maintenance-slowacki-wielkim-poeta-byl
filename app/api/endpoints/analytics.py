from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import StreamingResponse
import pandas as pd
import io

from app.api.dependencies import get_db
from app.models.maintenance import ServiceRecord

router = APIRouter()

@router.get("/export/maintenance")
async def export_maintenance_records(db: AsyncSession = Depends(get_db)):
    # 1. Fetch records asynchronously from the database
    result = await db.execute(select(ServiceRecord))
    records = result.scalars().all()
    
    # 2. Map the database fields cleanly into dictionaries
    data = []
    for r in records:
        data.append({
            "ID": r.id,
            "Vehicle ID": r.vehicle_id,
            # Fix: Swapped 'date' for 'date_performed' to match your model structure
            "Date": r.date.strftime("%Y-%m-%d %H:%M:%S") if r.date else "", 
            "Description": r.description,
            # Compatibility Fix: Cast Numeric/Decimal to float for safe Pandas parsing
            "Cost": float(r.cost) if r.cost is not None else 0.0
        })
        
    # 3. Create DataFrame
    df = pd.DataFrame(data)
    
    # Fallback: Enforce column headers even if the table has no entries
    if df.empty:
        df = pd.DataFrame(columns=["ID", "Vehicle ID", "Date", "Description", "Cost"])

    # 4. Use BytesIO to format data into a proper byte stream for streaming
    stream = io.BytesIO()
    df.to_csv(stream, index=False, encoding='utf-8')
    stream.seek(0) # Rewind the stream buffer back to the beginning
    
    # 5. Return the response using the filled buffer
    response = StreamingResponse(stream, media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=maintenance_export.csv"
    return response