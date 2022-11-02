# type: ignore[type-annotated]
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import backref, relationship
from datetime import datetime

from db.base_class import Base


class Set(Base):
    id = Column(Integer(), primary_key=True, index=True)
    user_id = Column(ForeignKey("tb_user.id"))
    title = Column(String(), nullable=False)
    description = Column(String(), nullable=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    user = relationship("User", backref=backref("sets", order_by=created_on))

    def __repr__(self):
        return (
            f"Set(id={self.id}, user_id={self.user_id}, "
            f"title={self.title}, description={self.description}, "
            f"created_on={self.created_on}, updated_on={self.updated_on})"
        )
