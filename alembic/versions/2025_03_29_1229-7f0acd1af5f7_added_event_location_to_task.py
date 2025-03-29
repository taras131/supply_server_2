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
    # Добавляем новый столбец `event_location_tmp` с нужными параметрами (nullable=False)
    op.add_column(
        "machinery_tasks",
        sa.Column(
            "event_location_tmp",
            sa.String(length=1024),
            nullable=False,
            server_default="",
        ),
    )

    # Копируем данные из старого столбца в новый
    op.execute(
        "UPDATE machinery_tasks SET event_location_tmp = COALESCE(event_location, '')"
    )

    # Удаляем старый столбец
    op.drop_column("machinery_tasks", "event_location")

    # Переименовываем новый столбец в `event_location`
    op.alter_column(
        "machinery_tasks",
        "event_location_tmp",
        new_column_name="event_location",
    )


def downgrade() -> None:
    # Добавляем обратно старый столбец
    op.add_column(
        "machinery_tasks",
        sa.Column("event_location", sa.String(length=1024), nullable=True),
    )

    # Копируем данные обратно
    op.execute("UPDATE machinery_tasks SET event_location = event_location_tmp")

    # Удаляем временный столбец
    op.drop_column("machinery_tasks", "event_location_tmp")
