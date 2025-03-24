from pydantic import BaseModel, ConfigDict
from api_v1.problems.schemas import ProblemSchema
from api_v1.tasks.schemas import TaskSchema
from typing import Optional
from typing import List


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
    text: str
    is_active: bool
    author_id: int
    machinery_id: int
    created_date: int
    updated_date: int
    rating: List[int]


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
    photos: List[str]
    vin: Optional[str] = None
    state_number: Optional[str] = None
    status: str
    engine_type_id: Optional[int] = None
    traction_type_id: Optional[int] = None
    transmission_type_id: Optional[int] = None
    operating_type_id: Optional[int] = None
    working_equipment: Optional[str] = None
    engine_brand: Optional[str] = None
    engine_model: Optional[str] = None
    transmission_brand: Optional[str] = None
    transmission_model: Optional[str] = None
    frame_number: Optional[str] = None


class MachineryCreateSchema(MachineryBaseSchema):
    pass


class MachinerySchema(MachineryBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_date: int
    updated_date: int
    comments: List[MachineryCommentSchema]
    photos: List[str]
    docs: List[DocsSchema]  # Добавляем docs
    tasks: List[TaskSchema]


class MachineryCompleteSchema(MachinerySchema):
    model_config = ConfigDict(from_attributes=True)
    docs: List[DocsSchema]
    tasks: List[TaskSchema]
    problems: List[ProblemSchema]


class MachineryUpdateSchema(MachineryCompleteSchema):
    pass
