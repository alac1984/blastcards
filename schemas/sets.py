from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SetCreate(BaseModel):
    title: str
    description: Optional[str]


class SetShow(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    created_on: datetime
    updated_on: datetime

    class Config:
        orm_mode = True
