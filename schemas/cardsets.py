from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CardsetCreate(BaseModel):
    title: str
    description: Optional[str]


class CardsetShow(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    created_on: datetime
    updated_on: datetime

    class Config:
        orm_mode = True
