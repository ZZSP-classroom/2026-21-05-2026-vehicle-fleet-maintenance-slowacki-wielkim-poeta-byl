from fastapi import FastAPI
from app.api.endpoints import vehicles, telemetry, analytics
from app.db.base import Base # Imports all models
from app.db.session import engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="VehicleFleetMaintenance")

app.include_router(vehicles.router, prefix="/api/vehicles", tags=["vehicles"])
app.include_router(telemetry.router, prefix="/api/telemetry", tags=["telemetry"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

@app.get("/")
def root():
    return {"message": "Welcome to VehicleFleetMaintenance API"}
