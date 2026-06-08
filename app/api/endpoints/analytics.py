from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import pandas as pd
import io

from app.api.dependencies import get_db
from app.models.maintenance import ServiceRecord

router = APIRouter()

@router.get("/export/maintenance")
def export_maintenance_records(db: Session = Depends(get_db)):
    records = db.query(ServiceRecord).all()
    
    data = []
    for r in records:
        data.append({
            "ID": r.id,
            "Vehicle ID": r.vehicle_id,
            "Date": r.date.strftime("%Y-%m-%d %H:%M:%S"),
            "Description": r.description,
            "Cost": r.cost
        })
        
    df = pd.DataFrame(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=maintenance_export.csv"
    return response
