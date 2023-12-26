from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class ContactModel(BaseModel):
    name: str = Field(max_length=70)
    surname: str = Field(max_length=70)
    email: str = EmailStr()  # must be unique
    phone: str = Field(max_length=50)
    date_of_birth: datetime
    additional_info: Optional[str] = Field(max_length=300)


class ContactResponse(ContactModel):
    id: int

    class Config:
        orm_mode = True
