from pydantic import BaseModel, ConfigDict
from typing import Optional
from typing import List
from api_v1.invoices.schemas import InvoicesSchema


class OrdersItemsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None
    catalogNumber: Optional[str] = None
    count: int
    comment: Optional[str] = None
    is_ordered: bool
    completionType: str
    photos: List[str]
    invoice_id: int
    ##invoice: Optional[InvoicesSchema] = None
    order_id: int


class OrdersBaseSchema(BaseModel):
    old_id: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
    author_id: Optional[int] = None
    title: str
    is_approved: bool
    approved_author_id: Optional[int] = None
    approved_date: Optional[int] = None
    assigned_to_id: Optional[int] = None
    shipment_type: str
    order_type: str
    comment: Optional[str] = None
    machinery_id: Optional[int] = None
    orders_items: List[OrdersItemsSchema]


class OrdersCreateSchema(OrdersBaseSchema):
    pass


class OrdersSchema(OrdersBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_date: int
    updated_date: int
    completion_percentage: Optional[int] = None


class OrdersUpdateSchema(OrdersSchema):
    pass
