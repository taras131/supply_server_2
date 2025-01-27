from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import datetime
from typing import Optional, List
from . import Machinery


class MachineryTask(Base):
    __tablename__ = "machinery_tasks"

    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(1024))
    status_id: Mapped[int]
    priority_id: Mapped[int]
    due_date: Mapped[int]
    issue_photos: Mapped[List[int]] = mapped_column(JSON, default=list)
    result_photos: Mapped[List[int]] = mapped_column(JSON, default=list)
    result_description: Mapped[str] = mapped_column(String(1024), default="")
    spent_resources: Mapped[str] = mapped_column(String(1024), default="")
    author_id: Mapped[int]
    assigned_to_id: Mapped[int]
    machinery_id: Mapped[int] = mapped_column(ForeignKey("machinery.id"), nullable=True)
    machinery: Mapped["Machinery"] = relationship(
        "Machinery", back_populates="tasks", lazy="selectin"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status_id": self.status_id,
            "priority_id": self.priority_id,
            "due_date": self.due_date,
            "machinery_id": self.machinery_id,
            "author": self.author_id,
            "assigned_to": self.assigned_to_id,
            "created_date": self.created_date,
            "updated_date": self.updated_date,
        }
