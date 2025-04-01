from sqlalchemy import Table, Column, ForeignKey
from .base import Base
from typing import TYPE_CHECKING, List


shipments_invoices_association = Table(
    "shipments_invoices",
    Base.metadata,
    Column("shipment_id", ForeignKey("shipments.id"), primary_key=True),
    Column(
        "invoice_id", ForeignKey("invoice.id"), primary_key=True
    ),  # ForeignKey для Invoices
    Column(
        "orders_item_id", ForeignKey("orders_items.id"), nullable=False
    ),  # ForeignKey для OrdersItems
)
