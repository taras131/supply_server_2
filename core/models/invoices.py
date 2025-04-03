from sqlalchemy import String, JSON, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import Optional, List, TYPE_CHECKING


if TYPE_CHECKING:
    from . import Shipments
    from . import Suppliers
    from . import OrdersItems


class Invoices(Base):
    __tablename__ = "invoice"

    old_id: Mapped[str] = mapped_column(String(100), default="", nullable=True)
    author_id: Mapped[int] = mapped_column(nullable=True)
    is_approved: Mapped[bool]
    approved_author_id: Mapped[int] = mapped_column(nullable=True)
    approved_date: Mapped[int] = mapped_column(nullable=True)
    is_paid: Mapped[bool]
    paid_author_id: Mapped[int] = mapped_column(nullable=True)
    paid_date: Mapped[int] = mapped_column(nullable=True)
    payment_order_patch: Mapped[str] = mapped_column(String(100), default="")
    number: Mapped[str] = mapped_column(String(1024))
    amount: Mapped[int]
    is_with_vat: Mapped[bool]
    request_id: Mapped[int] = mapped_column(nullable=True)
    is_full_shipment: Mapped[bool] = mapped_column(nullable=True)
    invoice_patch: Mapped[str] = mapped_column(String(1024))
    is_cancel: Mapped[bool]
    cancel_date: Mapped[int] = mapped_column(nullable=True)
    cancel_author_id: Mapped[int] = mapped_column(nullable=True)
    shipments_id: Mapped[List[int]] = mapped_column(JSON, default=[])
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    supplier: Mapped["Suppliers"] = relationship(
        "Suppliers", back_populates="invoices", lazy="joined"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "old_id": self.old_id,
            "author_id": self.author_id,
            "is_approved": self.is_approved,
            "approved_author_id": self.approved_author_id,
            "approved_date": self.approved_date,
            "is_paid": self.is_paid,
            "created_date": self.created_date,
            "paid_author_id": self.paid_author_id,
            "updated_date": self.updated_date,
            "paid_date": self.paid_date,
            "payment_order_patch": self.payment_order_patch,
            "number": self.number,
            "amount": self.amount,
            "is_with_vat": self.is_with_vat,
            "request_id": self.request_id,
            "supplier_id": self.supplier_id,
            "invoice_patch": self.invoice_patch,
            "is_cancel": self.is_cancel,
            "cancel_date": self.cancel_date,
            "cancel_author_id": self.cancel_author_id,
        }
