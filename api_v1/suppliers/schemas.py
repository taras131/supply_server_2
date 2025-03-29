from pydantic import BaseModel, ConfigDict
from typing import Optional
from typing import List


class SupplierBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    INN: int
    old_id: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    created_date: Optional[int] = None
    updated_date: Optional[int] = None
    manager_email: Optional[str] = None
    accounts_department_email: Optional[str] = None
    kpp: Optional[int] = None
    Legal_address: Optional[str] = None
    bik: Optional[int] = None
    correspondent_account: Optional[int] = None
    payment_account: Optional[int] = None
    bank: Optional[str] = None
    ogrn: Optional[int] = None
    okpo: Optional[int] = None
    okato: Optional[int] = None
    okogu: Optional[int] = None


class SupplierCreateSchema(SupplierBaseSchema):
    pass


class SupplierSchema(SupplierBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class SupplierUpdateSchema(SupplierBaseSchema):
    pass
