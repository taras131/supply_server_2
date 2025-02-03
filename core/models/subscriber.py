from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer, String, Boolean


class Subscriber(Base):
    __tablename__ = "subscribers"
    chat_id: Mapped[int] = Column(
        Integer, unique=True
    )  # Уникальный ID чата (например, Telegram chat_id)
    username: Mapped[str] = Column(String, nullable=True)
    is_active: Mapped[bool] = Column(Boolean, default=True)
