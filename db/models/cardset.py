# type: ignore[type-annotated]
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

from db.base_class import Base


class Cardset(Base):
    id = Column(Integer(), primary_key=True, index=True)
    user_id = Column(ForeignKey("tb_user.id"))
    title = Column(String(), nullable=False)
    description = Column(String(), nullable=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    user = relationship("User", backref=backref("cardsets", order_by=created_on))

    def __repr__(self):
        return (
            f"Cardset(id={self.id}, user_id={self.user_id}, "
            f"title={self.title}, description={self.description}, "
            f"created_on={self.created_on}, updated_on={self.updated_on})"
        )
