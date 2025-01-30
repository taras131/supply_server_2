from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import datetime
from typing import Optional, List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Machinery
    from . import MachineryProblem


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
    problem_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("machinery_problem.id"), nullable=True
    )
    problem: Mapped[Optional["MachineryProblem"]] = relationship(
        "MachineryProblem", lazy="selectin"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status_id": self.status_id,
            "priority_id": self.priority_id,
            "due_date": self.due_date,
            "issue_photos": self.issue_photos,
            "result_photos": self.result_photos,
            "result_description": self.result_description,
            "spent_resources": self.spent_resources,
            "author_id": self.author_id,
            "assigned_to_id": self.assigned_to_id,
            "problem_id": self.problem_id,
            "created_date": self.created_date,
            "updated_date": self.updated_date,
        }
