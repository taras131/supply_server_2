from sqlalchemy import Table, Column, ForeignKey
from .base import Base

# Ассоциативная таблица для связи "многие ко многим"
shipments_invoices_association = Table(
    "shipments_invoices",
    Base.metadata,
    Column("shipment_id", ForeignKey("shipments.id"), primary_key=True),
    Column("invoice_id", ForeignKey("invoice.id"), primary_key=True),
)
