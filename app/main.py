from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.endpoints import vehicles, telemetry, analytics, inventory
from app.db.base import Base # Imports all models
from app.db.session import engine
import app.api.endpoints.auth as auth
import app.api.endpoints.reports as reports

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create DB tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="VehicleFleetMaintenance", lifespan=lifespan)

# CORS middleware configuration
origins = [
    "http://localhost:3000",
    "*" # For development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(vehicles.router, prefix="/api/vehicles", tags=["vehicles"])
app.include_router(telemetry.router, prefix="/api/telemetry", tags=["telemetry"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(inventory.router, prefix="/parts", tags=["inventory"])

@app.get("/")
def root():
    return {"message": "Welcome to VehicleFleetMaintenance API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
