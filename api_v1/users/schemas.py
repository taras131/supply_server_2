from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserAuthSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password: str


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    first_name: str
    middle_name: str
    role_id: int


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class UserCreateSchema(UserAuthSchema):
    first_name: str
    middle_name: str
    role_id: int
