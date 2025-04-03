from pydantic import BaseModel, ConfigDict
from typing import Optional
from typing import List
from api_v1.suppliers.schemas import SupplierSchema


class InvoicesBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    old_id: Optional[str] = None
    author_id: Optional[int] = None
    is_approved: bool
    approved_author_id: Optional[int] = None
    approved_date: Optional[int] = None
    is_paid: bool
    paid_author_id: Optional[int] = None
    paid_date: Optional[int] = None
    payment_order_patch: Optional[str] = None
    number: str
    amount: int
    is_with_vat: bool
    request_id: Optional[int] = None
    shipment_id: Optional[int] = None
    is_full_shipment: bool
    invoice_patch: str
    is_cancel: bool
    cancel_date: Optional[int] = None
    cancel_author_id: Optional[int] = None
    supplier_id: int
    created_date: Optional[int] = None


class InvoicesCreateSchema(InvoicesBaseSchema):
    pass


class InvoicesSchema(InvoicesBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_date: int
    updated_date: int
    supplier: List[SupplierSchema]


class InvoicesUpdateSchema(InvoicesSchema):
    pass
