from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
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
    date_of_birth: Mapped[str] = mapped_column(DateTime)
    additional_info: Mapped[str] = mapped_column(String(300), nullable=True)
