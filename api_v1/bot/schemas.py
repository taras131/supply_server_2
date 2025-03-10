from pydantic import BaseModel


class SubscriberCreateSchema(BaseModel):
    chat_id: int
    username: str | None = None
    is_active: bool = True
