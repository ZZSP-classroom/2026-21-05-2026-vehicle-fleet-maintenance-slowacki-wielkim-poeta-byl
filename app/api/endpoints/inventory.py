from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy.future import select
from app.api.dependencies import get_db
from app.models.part import Part as PartModel
from app.schemas.part import Part, PartCreate

router = APIRouter()

@router.post("/", response_model=Part)
async def create_part(part: PartCreate, db: AsyncSession = Depends(get_db)):
    db_part = PartModel(**part.model_dump())
    db.add(db_part)
    await db.commit()
    await db.refresh(db_part)
    return db_part

@router.get("/", response_model=List[Part])
async def read_parts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PartModel).offset(skip).limit(limit))
    return result.scalars().all()
