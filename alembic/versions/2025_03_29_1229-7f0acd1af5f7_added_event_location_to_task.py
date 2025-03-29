"""added event location to task

Revision ID: 7f0acd1af5f7
Revises: 86ddfc6c78ab
Create Date: 2025-03-29 12:29:49.675764

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7f0acd1af5f7"
down_revision: Union[str, None] = "86ddfc6c78ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем новый обязательный столбец
    op.add_column(
        "machinery_tasks",
        sa.Column(
            "event_location", sa.String(length=1024), nullable=True
        ),  # Добавляем поле как nullable
    )

    # Устанавливаем значение по умолчанию для существующих строк
    op.execute("UPDATE machinery_tasks SET event_location = ''")

    # После обновления всех строк делаем поле обязательным (nullable=False)
    op.alter_column(
        "machinery_tasks",
        "event_location",
        existing_type=sa.String(length=1024),
        nullable=False,
    )


def downgrade() -> None:
    op.drop_column("machinery_tasks", "event_location")
