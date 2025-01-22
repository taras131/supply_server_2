from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger
from typing import Optional
from typing import List

from api_v1.tasks.schemas import TaskSchema


class MachineryCommentBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str
    is_active: bool
    author_id: int
    machinery_id: int


class MachineryCommentCreateSchema(MachineryCommentBaseSchema):
    pass


class MachineryCommentSchema(MachineryCommentBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    rating: List[int]
    created_date: int
    updated_date: int


class MachineryCommentUpdateSchema(MachineryCommentSchema):
    pass


class DocsBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    file_name: str
    machinery_id: int


class DocsCreateSchema(DocsBaseSchema):
    pass


class DocsUpdateSchema(DocsBaseSchema):
    pass


class DocsSchema(DocsBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_date: int
    updated_date: int


class MachineryBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    brand: str
    model: str
    year_manufacture: int
    type_id: int
    vin: Optional[str] = None
    state_number: Optional[str] = None
    status: str


class MachineryCreateSchema(MachineryBaseSchema):
    pass


class MachinerySchema(MachineryBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_date: int
    updated_date: int
    comments: List[MachineryCommentSchema]
    photos: List[str]


class MachineryCompleteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    brand: str
    model: str
    year_manufacture: int
    type_id: int
    vin: Optional[str] = None
    state_number: Optional[str] = None
    status: str
    id: int
    created_date: int
    updated_date: int
    comments: List[MachineryCommentSchema]
    photos: List[str]
    docs: List[DocsSchema]
    tasks: List[TaskSchema]


class MachineryUpdateSchema(MachinerySchema):
    pass
