"""Add orders table

Revision ID: 1eb22cd7bf56
Revises: b241f21bd0f8
Create Date: 2025-04-01 15:54:16.231936

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1eb22cd7bf56"
down_revision: Union[str, None] = "b241f21bd0f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем новые колонки
    op.add_column("invoice", sa.Column("is_full_shipment", sa.Boolean(), nullable=True))
    op.add_column("machinery", sa.Column("old_id", sa.String(), nullable=False, server_default=""))
    op.add_column("orders", sa.Column("old_id", sa.String(), nullable=False, server_default=""))
    op.add_column("shipments", sa.Column("photos", sa.JSON(), nullable=False))

    # Используем batch mode для изменения foreign key в таблице orders_items
    with op.batch_alter_table("orders_items", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.create_foreign_key(None, "orders", ["order_id"], ["id"])

    # Устанавливаем старым записям в таблице machinery значение old_id = ''
    op.execute("UPDATE machinery SET old_id = ''")

    # Устанавливаем старым записям в таблице orders значение old_id = ''
    op.execute("UPDATE orders SET old_id = ''")

    # Удаляем временный server_default для колонок old_id
    op.alter_column("machinery", "old_id", server_default=None)
    op.alter_column("orders", "old_id", server_default=None)


def downgrade() -> None:
    # Удаляем все изменения, произведенные в upgrade
    with op.batch_alter_table("orders_items", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.create_foreign_key(None, "machinery", ["order_id"], ["id"])

    op.drop_column("shipments", "photos")
    op.drop_column("orders", "old_id")
    op.drop_column("machinery", "old_id")
    op.drop_column("invoice", "is_full_shipment")
