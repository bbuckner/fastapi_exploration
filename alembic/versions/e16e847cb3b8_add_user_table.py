"""add user table

Revision ID: e16e847cb3b8
Revises: 32f336f5b34f
Create Date: 2022-12-12 05:16:39.568863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e16e847cb3b8"
down_revision = "32f336f5b34f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        # Can also do this by passing primary_key=True in the column itself.
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")
