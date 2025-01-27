"""migration task to machinery

Revision ID: 5af26f4675c6
Revises: 3a46a93baa6b
Create Date: 2025-01-27 12:34:17.201293

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = "5af26f4675c6"
down_revision: Union[str, None] = "3a46a93baa6b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "machinery_tasks",
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.Column("priority_id", sa.Integer(), nullable=False),
        sa.Column("due_date", sa.Integer(), nullable=False),
        sa.Column("issue_photos", sa.JSON(), nullable=False),
        sa.Column("result_photos", sa.JSON(), nullable=False),
        sa.Column("result_description", sa.String(length=1024), nullable=False),
        sa.Column("spent_resources", sa.String(length=1024), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("assigned_to_id", sa.Integer(), nullable=False),
        sa.Column("machinery_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_date", sa.BigInteger(), nullable=False),
        sa.Column("updated_date", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["machinery_id"],
            ["machinery.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("tasks")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tasks",
        sa.Column("title", sa.VARCHAR(length=128), nullable=False),
        sa.Column("description", sa.VARCHAR(length=1024), nullable=False),
        sa.Column("status_id", sa.INTEGER(), nullable=False),
        sa.Column("priority_id", sa.INTEGER(), nullable=False),
        sa.Column("due_date", sa.INTEGER(), nullable=False),
        sa.Column("issue_photos", sqlite.JSON(), nullable=False),
        sa.Column("result_photos", sqlite.JSON(), nullable=False),
        sa.Column("result_description", sa.VARCHAR(length=1024), nullable=False),
        sa.Column("spent_resources", sa.VARCHAR(length=1024), nullable=False),
        sa.Column("author_id", sa.INTEGER(), nullable=False),
        sa.Column("assigned_to_id", sa.INTEGER(), nullable=False),
        sa.Column("machinery_id", sa.INTEGER(), nullable=True),
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("created_date", sa.BIGINT(), nullable=False),
        sa.Column("updated_date", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(
            ["machinery_id"],
            ["machinery.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("machinery_tasks")
    # ### end Alembic commands ###
