from .base import Base
from sqlalchemy import String, JSON
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
    relationship,
)
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .invoices import Invoices


class Suppliers(Base):
    __tablename__ = "suppliers"

    name: Mapped[str] = mapped_column(String(100))
    INN: Mapped[int] = mapped_column(nullable=True)
    old_id: Mapped[str] = mapped_column(String(100), default="", nullable=True)
    city: Mapped[str] = mapped_column(String(32), default="")
    phone: Mapped[str] = mapped_column(String(32), default="")
    manager_email: Mapped[str] = mapped_column(String(64), default="")
    accounts_department_email: Mapped[str] = mapped_column(String(64), default="")
    kpp: Mapped[int] = mapped_column(nullable=True)
    Legal_address: Mapped[str] = mapped_column(String(600), default="")
    bik: Mapped[int] = mapped_column(nullable=True)
    correspondent_account: Mapped[int] = mapped_column(nullable=True)
    payment_account: Mapped[int] = mapped_column(nullable=True)
    bank: Mapped[str] = mapped_column(String(600), default="")
    ogrn: Mapped[int] = mapped_column(nullable=True)
    okpo: Mapped[int] = mapped_column(nullable=True)
    okato: Mapped[int] = mapped_column(nullable=True)
    okogu: Mapped[int] = mapped_column(nullable=True)
    invoices: Mapped[List["Invoices"]] = relationship(
        "Invoices",
        back_populates="supplier",
        lazy="selectin",
        collection_class=list,
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "INN": self.INN,
            "old_id": self.old_id,
            "city": self.city,
            "phone": self.phone,
            "manager_email": self.manager_email,
            "accounts_department_email": self.accounts_department_email,
            "kpp": self.kpp,
            "Legal_address": self.Legal_address,
            "created_date": self.created_date,
            "updated_date": self.updated_date,
            "bik": self.bik,
            "correspondent_account": self.correspondent_account,
            "payment_account": self.payment_account,
            "bank": self.bank,
            "ogrn": self.ogrn,
            "okpo": self.okpo,
            "okato": self.okato,
            "okogu": self.okogu,
        }
