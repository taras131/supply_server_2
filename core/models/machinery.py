from .base import Base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Machinery(Base):
    __tablename__ = "machinery"

    brand: Mapped[str]
    model: Mapped[str]
    year_manufacture: Mapped[int]
    machinery_type_id: Mapped[int]
    vin: Mapped[str]
    state_number: Mapped[str]
    status: Mapped[str]
