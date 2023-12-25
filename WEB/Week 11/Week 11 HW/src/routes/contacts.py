from fastapi import APIRouter
from sqlalchemy.orm import AsyncSession

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/tags', tags=["tags"])
