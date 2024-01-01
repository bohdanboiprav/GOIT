from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.database.models import User
from src.schemas.user import UserModel


async def get_user_by_email(email: str, db: AsyncSession):
    user = select(User).filter(User.email == email)
    user = await db.execute(user)
    return user.scalars().first()


async def create_user(body: UserModel, db: AsyncSession):
    try:
        gravatar = Gravatar(body.email)
        avatar = gravatar.get_image(size=200, default='identicon')
    except Exception as e:
        print(e)
        avatar = None
    user = User(username=body.username, email=body.email, password=body.password, avatar=avatar)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    user.refresh_token = token
    await db.commit()


async def confirm_email(email: str, db: AsyncSession) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()
