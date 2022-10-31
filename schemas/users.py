from pydantic import BaseModel
from pydantic import EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class ShowSuperuser(BaseModel):
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True
