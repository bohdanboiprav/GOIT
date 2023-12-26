from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, PastDate


class ContactModel(BaseModel):
    name: str = Field(max_length=70)
    surname: str = Field(max_length=70)
    email: str = EmailStr()
    phone: str = Field(max_length=50)
    date_of_birth: date = PastDate()
    additional_info: Optional[str] = Field(max_length=300)


class ContactResponse(BaseModel):
    id: int
    name: str = Field(max_length=70)
    surname: str = Field(max_length=70)
    email: str = EmailStr()
    phone: str = Field(max_length=50)
    date_of_birth: date = PastDate()
    additional_info: Optional[str] = Field(max_length=300)

    class Config:
        orm_mode = True
