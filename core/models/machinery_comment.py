from .base import Base
from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .machinery import Machinery


class MachineryComment(Base):
    __tablename__ = "machinery_comment"
    text: Mapped[str] = mapped_column(String(400))
    is_active: Mapped[bool]
    author_id: Mapped[int]
    rating: Mapped[List[int]] = mapped_column(JSON, default=list)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "is_active": self.is_active,
            "author_id": self.author_id,
            "rating": self.rating,
            # добавьте остальные поля
        }

    machinery_id: Mapped[int] = mapped_column(
        ForeignKey("machinery.id"),
        nullable=False,
    )
    machinery: Mapped["Machinery"] = relationship(
        "Machinery", back_populates="comments", lazy="selectin"
    )
