from .base import Base
from sqlalchemy import String, JSON
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
    relationship,
)
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .machinery_comment import MachineryComment
    from .machinery_docs import MachineryDocs
    from .machinery_tasks import MachineryTask
    from .machinery_problem import MachineryProblem


class Machinery(Base):
    __tablename__ = "machinery"
    brand: Mapped[str] = mapped_column(String(32))
    model: Mapped[str] = mapped_column(String(32))
    year_manufacture: Mapped[int]
    type_id: Mapped[int]
    vin: Mapped[str] = mapped_column(String(32))
    state_number: Mapped[str] = mapped_column(String(32), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=True)
    photos: Mapped[List[int]] = mapped_column(JSON, default=list)
    traction_type_id: Mapped[int] = mapped_column(nullable=True)
    engine_type_id: Mapped[int] = mapped_column(nullable=True)
    transmission_type_id: Mapped[int] = mapped_column(nullable=True)
    working_equipment: Mapped[str] = mapped_column(String(32), nullable=True)
    engine_brand: Mapped[str] = mapped_column(String(32), nullable=True)
    engine_model: Mapped[str] = mapped_column(String(32), nullable=True)
    transmission_brand: Mapped[str] = mapped_column(String(32), nullable=True)
    transmission_model: Mapped[str] = mapped_column(String(32), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "year_manufacture": self.year_manufacture,
            "type_id": self.type_id,
            "vin": self.vin,
            "state_number": self.state_number,
            "status": self.status,
            "photos": self.photos,
            "created_date": self.created_date,
            "updated_date": self.updated_date,
            "engine_type_id": self.engine_type_id,
            "traction_type_id": self.traction_type_id,
            "transmission_type_id": self.transmission_type_id,
            "working_equipment": self.working_equipment,
            "engine_brand": self.engine_brand,
            "engine_model": self.engine_model,
            "transmission_brand": self.transmission_brand,
            "transmission_model": self.transmission_model,
        }

    comments: Mapped[List["MachineryComment"]] = relationship(
        "MachineryComment",
        back_populates="machinery",
        lazy="selectin",
    )
    docs: Mapped[List["MachineryDocs"]] = relationship(
        "MachineryDocs",
        back_populates="machinery",
        lazy="selectin",
    )
    tasks: Mapped[List["MachineryTask"]] = relationship(
        "MachineryTask",
        back_populates="machinery",
        lazy="selectin",
        collection_class=list,
        cascade="all, delete-orphan",
    )
    problems: Mapped[List["MachineryTask"]] = relationship(
        "MachineryProblem",
        back_populates="machinery",
        lazy="selectin",
        collection_class=list,
        cascade="all, delete-orphan",
    )
