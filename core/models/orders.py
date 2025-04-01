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
    from .machinery import Machinery
    from .orders_items import OrdersItems


class Orders(Base):
    __tablename__ = "orders"

    old_id: Mapped[str] = mapped_column(default="", nullable=True)
    author_id: Mapped[int] = mapped_column(nullable=True)
    title: Mapped[str]
    is_approved: Mapped[bool]
    approved_author_id: Mapped[int] = mapped_column(nullable=True)
    approved_date: Mapped[int] = mapped_column(nullable=True)
    assigned_to_id: Mapped[int] = mapped_column(nullable=True)
    shipment_type: Mapped[str]
    order_type: Mapped[str]
    comment: Mapped[str] = mapped_column(default="")
    machinery_id: Mapped[int] = mapped_column(ForeignKey("machinery.id"), nullable=True)
    machinery: Mapped["Machinery"] = relationship(
        "Machinery", back_populates="orders", lazy="selectin"
    )
    orders_items: Mapped[List["OrdersItems"]] = relationship(
        "OrdersItems",
        back_populates="order",
        lazy="selectin",
        collection_class=list,
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "old_id": self.old_id,
            "author_id": self.author_id,
            "title": self.title,
            "is_approved": self.is_approved,
            "approved_author_id": self.approved_author_id,
            "approved_date": self.approved_date,
            "assigned_to_id": self.assigned_to_id,
            "shipment_type": self.shipment_type,
            "order_type": self.order_type,
            "comment": self.comment,
            "created_date": self.created_date,
            "updated_date": self.updated_date,
            "machinery_id": self.machinery_id,
        }
