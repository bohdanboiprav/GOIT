import datetime

from faker import Faker
import random
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas import ContactModel, ContactResponse

fake = Faker()


async def populate_contacts(count: int, db: AsyncSession):
    for _ in range(count):
        contact = Contact(name=fake.first_name(), surname=fake.last_name(), email=fake.email(),
                          phone=fake.phone_number(), date_of_birth=fake.date_of_birth(),
                          additional_info=fake.text() if random.randint(0, 1) == 1 else None)
        db.add(contact)
    await db.commit()
    return "Contacts populated"


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    contacts = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(contacts)
    return contacts.scalars().all()


async def get_contacts_by(name: str, surname: str, email: str, db: AsyncSession):
    contacts = select(Contact)
    if name:
        contacts = contacts.filter(Contact.name == name)
    if surname:
        contacts = contacts.filter(Contact.surname == surname)
    if email:
        contacts = contacts.filter(Contact.email == email)
    contacts = await db.execute(contacts)
    return contacts.scalars().all()


async def get_contacts_birthdays(db: AsyncSession):
    today = datetime.date.today()  # - datetime.timedelta(days=7)
    seven_days_later = today + datetime.timedelta(days=7)
    contacts = select(Contact)
    return_data = []
    contacts = await db.execute(contacts)
    for contact in contacts.scalars().all():
        birthday = contact.date_of_birth
        birthday = birthday.replace(year=today.year)
        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)
        if today <= birthday <= seven_days_later:
            return_data.append(contact)
    return return_data


async def get_contact(contact_id: int, db: AsyncSession):
    contact = select(Contact).filter(Contact.id == contact_id)
    contact = await db.execute(contact)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactModel, db: AsyncSession):
    contact = Contact(name=body.name, surname=body.surname, email=body.email, phone=body.phone,
                      date_of_birth=body.date_of_birth, additional_info=body.additional_info)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: AsyncSession):
    contact = select(Contact).filter(Contact.id == contact_id)
    result = await db.execute(contact)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.date_of_birth = body.date_of_birth
        contact.additional_info = body.additional_info
        await db.commit()
        await db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: AsyncSession):
    contact = select(Contact).filter(Contact.id == contact_id)
    result = await db.execute(contact)
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
