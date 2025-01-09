from pydantic import BaseModel, EmailStr
from typing import Annotated
from annotated_types import MinLen , MaxLen

class CreateUser(BaseModel):
    first_name: Annotated[str, MinLen(2), MaxLen(20)]
    middle_name: Annotated[str, MinLen(2), MaxLen(20)]
    role_id: int
    email: EmailStr