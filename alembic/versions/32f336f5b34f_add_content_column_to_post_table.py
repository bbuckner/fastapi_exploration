"""add content column to post table

Revision ID: 32f336f5b34f
Revises: fa42f2059d5b
Create Date: 2022-12-12 05:11:46.735036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "32f336f5b34f"
down_revision = "fa42f2059d5b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
