from datetime import datetime

from pydantic import BaseModel
from pydantic import EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class ShowSuperuser(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_on: datetime
    updated_on: datetime

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_on: datetime
    updated_on: datetime

    class Config:
        orm_mode = True
