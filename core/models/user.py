from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, declared_attr
from sqlalchemy import String


class User(Base):
    first_name: Mapped[str] = mapped_column(String(32))
    middle_name: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(32), unique=True)
    role_id: Mapped[int]
    password: Mapped[str] = mapped_column(String(128))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "email": self.email,
            "role_id": self.role_id,
            "created_date": self.created_date,
            "updated_date": self.updated_date,
        }
