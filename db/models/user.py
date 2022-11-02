from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from db.base_class import Base


class User(Base):
    id = Column(Integer(), primary_key=True, index=True)
    username = Column(String(), unique=True, nullable=False)
    email = Column(String(), nullable=False, unique=True, index=True)
    hashed_password = Column(String(), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return (
            f"User(id={self.id}, username={self.username}, "
            f"email={self.email}, is_active={self.is_active}, "
            f"is_superuser={self.is_superuser}, created_on={self.created_on}, "
            f"updated_on={self.updated_on}"
        )
