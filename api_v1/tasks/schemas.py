from pydantic import BaseModel, ConfigDict
from typing import Optional
from typing import List


class TaskBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    type_id: int
    status_id: int
    priority_id: int
    due_date: int
    issue_photos: List[str]
    author_id: int
    assigned_to_id: int
    machinery_id: Optional[int]
    issue_operating: Optional[int] = None
    issue_odometer: Optional[int] = None
    result_odometer: Optional[int] = None
    result_operating: Optional[int] = None
    problem_id: Optional[int] = None


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
