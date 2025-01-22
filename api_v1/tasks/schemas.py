from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger
from typing import Optional
from typing import List


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
