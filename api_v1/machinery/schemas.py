from pydantic import BaseModel, ConfigDict


class MachineryBase(BaseModel):
    brand: str
    model: str
    year_manufacture: int
    machinery_type_id: int
    vin: str
    state_number: str
    status: str


class MachineryCreate(MachineryBase):
    pass


class MachineryUpdate(MachineryCreate):
    pass


class Machinery(MachineryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
