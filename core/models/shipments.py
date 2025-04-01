from sqlalchemy import String, JSON, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import Optional, List, TYPE_CHECKING
from .shipments_invoices import shipments_invoices_association

if TYPE_CHECKING:
    from . import Invoices


class Shipments(Base):
    __tablename__ = "shipments"

    old_id: Mapped[str] = mapped_column(String(100), default="")
    author_id: Mapped[int] = mapped_column(nullable=True)
    is_received: Mapped[bool] = mapped_column(nullable=False)
    received_author_id: Mapped[int] = mapped_column(nullable=True)
    received_date: Mapped[int] = mapped_column(nullable=True)
    lading_number: Mapped[str] = mapped_column(default="")
    lading_file_path: Mapped[str] = mapped_column(default="")
    transporter: Mapped[str]
    type: Mapped[str]
    photos: Mapped[List[int]] = mapped_column(JSON, default=list)
    invoices_id: Mapped[List[int]] = mapped_column(JSON, default=list)
    invoices: Mapped[List["Invoices"]] = relationship(
        "Invoices",
        secondary=shipments_invoices_association,  # Промежуточная таблица
        back_populates="shipments",
        lazy="selectin",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "old_id": self.old_id,
            "author_id": self.author_id,
            "is_received": self.is_received,
            "received_author_id": self.received_author_id,
            "received_date": self.received_date,
            "lading_number": self.lading_number,
            "created_date": self.created_date,
            "lading_file_path": self.lading_file_path,
            "updated_date": self.updated_date,
            "transporter": self.transporter,
            "type": self.type,
            "photos": self.photos,
            "invoices_id": self.invoices_id,
            "invoices": [invoice.to_dict() for invoice in self.invoices],
        }
