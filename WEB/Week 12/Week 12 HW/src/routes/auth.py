from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/auth', tags=["auth"])


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(10, ge=2, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db)):
    return await repository_contacts.get_contacts(limit, offset, db)
