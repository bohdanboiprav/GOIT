from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas import ContactModel, ContactResponse


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    contacts = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(contacts)
    return contacts.scalars().all()


async def get_contact(contact_id, db: AsyncSession):
    contacts = select(Contact).filter(Contact.id == contact_id)
    contacts = await db.execute(contacts)
    return contacts.scalars().all()


async def create_contact(body: ContactModel, db: AsyncSession):
    contact = Contact(name=body.name, surname=body.surname, email=body.email, phone=body.phone,
                      date_of_birth=body.date_of_birth, additional_info=body.additional_info)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact
