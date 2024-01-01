from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.schemas.contact import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(10, ge=2, le=500), offset: int = Query(0, ge=0),
                       current_user: User = Depends(auth_service.get_current_user),
                       db: AsyncSession = Depends(get_db)):
    return await repository_contacts.get_contacts(current_user, limit, offset, db)


@router.get("/by", response_model=list[ContactResponse])
async def get_contacts_by(name: str = Query(None, min_length=1, max_length=70),
                          surname: str = Query(None, min_length=1, max_length=70),
                          email: str = Query(None, min_length=1, max_length=70),
                          current_user: User = Depends(auth_service.get_current_user),
                          db: AsyncSession = Depends(get_db)):
    return await repository_contacts.get_contacts_by(name, surname, email, current_user, db)


@router.get("/birthdays", response_model=list[ContactResponse])
async def get_contacts_by(current_user: User = Depends(auth_service.get_current_user),
                          db: AsyncSession = Depends(get_db)):
    return await repository_contacts.get_contacts_birthdays(current_user, db)


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user),
                      db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found")
    return contact


@router.post("/create", response_model=ContactResponse)
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user),
                         db: AsyncSession = Depends(get_db)):
    return await repository_contacts.create_contact(body, current_user, db)


@router.post("/populate/{count}")
async def populate_contact(count: int = Path(ge=1, le=150), current_user: User = Depends(auth_service.get_current_user),
                           db: AsyncSession = Depends(get_db)):
    return await repository_contacts.populate_contacts(count, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1),
                         current_user: User = Depends(auth_service.get_current_user),
                         db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact is not found")
    return contact
