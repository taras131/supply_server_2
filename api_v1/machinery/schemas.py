from pydantic import BaseModel, ConfigDict
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


class TaskBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    status_id: int
    priority_id: int
    due_date: int
    issue_photos: List[str]
    author_id: int
    assigned_to_id: int
    machinery_id: Optional[int]


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskSchema(TaskBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_date: int
    updated_date: int
    result_description: str
    spent_resources: str
    result_photos: List[str]


class TaskUpdateSchema(TaskSchema):
    pass


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
