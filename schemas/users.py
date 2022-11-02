from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class ShowSuperuser(BaseModel):
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_on: datetime
    updated_on: datetime

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    username: str
    email: EmailStr
    is_active: bool
    created_on: datetime
    updated_on: datetime

    class Config:
        orm_mode = True
