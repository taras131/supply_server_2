from .base import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
    relationship,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .machinery import Machinery


class MachineryDocs(Base):
    __tablename__ = "machinery_docs"
    title: Mapped[str] = mapped_column(String(32))
    file_name: Mapped[str] = mapped_column(String(400))
    machinery_id: Mapped[int] = mapped_column(
        ForeignKey("machinery.id"),
        nullable=False,
    )
    machinery: Mapped["Machinery"] = relationship(
        "Machinery", back_populates="docs", lazy="selectin"
    )
