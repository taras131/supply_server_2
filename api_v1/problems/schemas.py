from pydantic import BaseModel, ConfigDict
from typing import Optional
from typing import List


class ProblemBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    photos: List[str]
    author_id: int
    machinery_id: int
    priority_id: int
    category_id: int
    status_id: int
    operating: Optional[int] = None
    odometer: Optional[int] = None
    tasks_id: List[int]


class ProblemCreateSchema(ProblemBaseSchema):
    pass


class ProblemSchema(ProblemBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_date: int
    updated_date: int


class ProblemUpdateSchema(ProblemSchema):
    pass
