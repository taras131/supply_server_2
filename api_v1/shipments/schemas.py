from pydantic import BaseModel, ConfigDict
from typing import Optional
from typing import List
from api_v1.invoices.schemas import InvoicesSchema


class ShipmentsBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    old_id: Optional[str] = None
    author_id: Optional[str] = None
    is_received: bool
    received_author_id: Optional[int] = None
    received_date: Optional[int] = None
    lading_number: str
    lading_file_path: Optional[str] = None
    transporter: str
    type: str
    photos: List[str]
    invoices_id: List[int]


class ShipmentsCreateSchema(ShipmentsBaseSchema):
    pass


class ShipmentsSchema(ShipmentsBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_date: int
    updated_date: int
    invoices: List[InvoicesSchema]


class ShipmentsUpdateSchema(ShipmentsSchema):
    pass
