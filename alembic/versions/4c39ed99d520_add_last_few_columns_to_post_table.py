"""add last few columns to post table

Revision ID: 4c39ed99d520
Revises: 1abc26d0086b
Create Date: 2022-12-12 05:29:36.921347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4c39ed99d520"
down_revision = "1abc26d0086b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="true"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
