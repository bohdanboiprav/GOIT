from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.database.models import User
from src.schemas.user import UserModel


async def get_user_by_email(email: str, db: AsyncSession):
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user with that email. If no such user exists, it returns None.

    :param email: str: Pass in the email address of the user we want to get from the database
    :param db: AsyncSession: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    user = select(User).filter(User.email == email)
    user = await db.execute(user)
    return user.scalars().first()


async def create_user(body: UserModel, db: AsyncSession):
    """
    The create_user function creates a new user in the database.

    :param body: UserModel: Get the data from the request body
    :param db: AsyncSession: Pass the database session into the function
    :return: A user object
    :doc-author: Trelent
    """
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
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Specify the user object that is being updated
    :param token: str | None: Update the refresh token in the database
    :param db: AsyncSession: Pass the database session to the function
    :return: None
    :doc-author: Trelent
    """
    user.refresh_token = token
    await db.commit()


async def confirm_email(email: str, db: AsyncSession) -> None:
    """
    The confirm_email function takes an email and a database session as arguments.
    It then gets the user with that email from the database, sets their confirmed field to True,
    and commits those changes to the database.

    :param email: str: Get the user by email
    :param db: AsyncSession: Pass the database session to the function
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar(email: EmailStr, src_url: str, db: AsyncSession):
    """
    The update_avatar function updates the avatar of a user.

    :param email: EmailStr: Get the user by email
    :param src_url: str: Get the source url of the avatar image
    :param db: AsyncSession: Pass in the database session
    :return: The user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = src_url
    await db.commit()
    await db.refresh(user)
    return user
