from .base import Base
from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
    relationship,
)
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .orders import Orders


class OrdersItems(Base):
    __tablename__ = "orders_items"

    name: Mapped[str] = mapped_column(default="")
    catalogNumber: Mapped[str] = mapped_column(default="")
    count: Mapped[int]
    comment: Mapped[str] = mapped_column(default="")
    is_ordered: Mapped[bool]
    completionType: Mapped[str] = mapped_column(default="")
    photos: Mapped[List[int]] = mapped_column(JSON, default=list)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoice.id"), nullable=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=True)
    order: Mapped["Orders"] = relationship(
        "Orders", back_populates="orders_items", lazy="selectin"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "catalogNumber": self.catalogNumber,
            "count": self.count,
            "comment": self.comment,
            "is_ordered": self.is_ordered,
            "completionType": self.completionType,
            "photos": self.photos,
            "invoice_id": self.invoice_id,
            "created_date": self.created_date,
            "order_id": self.order_id,
            "order": self.order,
        }
