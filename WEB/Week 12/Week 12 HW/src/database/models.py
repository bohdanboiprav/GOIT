import enum
import uuid
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, func, DateTime, Enum, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(70), index=True)
    surname: Mapped[str] = mapped_column(String(70), index=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(50))
    date_of_birth: Mapped[str] = mapped_column(Date)
    additional_info: Mapped[str] = mapped_column(String(300), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    user: Mapped["User"] = relationship("User", backref="todos", lazy="joined")


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50))
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    role: Mapped[Enum] = mapped_column('role', Enum(Role), default=Role.user, nullable=True)
