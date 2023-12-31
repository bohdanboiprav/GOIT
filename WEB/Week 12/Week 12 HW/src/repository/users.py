import datetime

import random
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas import ContactModel, ContactResponse


async def get_user_by_email(email: str, db: AsyncSession):
    user = select(Contact).filter(Contact.email == email)
    user = await db.execute(user)
    return user.scalars().first()

