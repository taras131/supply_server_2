from sqlalchemy import String, JSON, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from . import Machinery
    from . import MachineryTask


class MachineryProblem(Base):
    __tablename__ = "machinery_problem"

    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(1024))
    priority_id: Mapped[int]
    photos: Mapped[List[int]] = mapped_column(JSON, default=list)
    author_id: Mapped[int]
    category_id: Mapped[int]
    subcategory_id: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    machinery_id: Mapped[int] = mapped_column(ForeignKey("machinery.id"), nullable=True)
    machinery: Mapped["Machinery"] = relationship(
        "Machinery", back_populates="problems", lazy="selectin"
    )
    task: Mapped[Optional["MachineryTask"]] = relationship(
        "MachineryTask",
        back_populates="problem",
        lazy="selectin",  # или "joined"
        uselist=False,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority_id": self.priority_id,
            "photos": self.photos,
            "author_id": self.author_id,
            "machinery_id": self.machinery_id,
            "created_date": self.created_date,
            "updated_date": self.updated_date,
            "task": self.task.id if self.task else None,
        }
