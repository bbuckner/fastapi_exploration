"""add foreign key to post table

Revision ID: 1abc26d0086b
Revises: e16e847cb3b8
Create Date: 2022-12-12 05:25:16.893164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1abc26d0086b"
down_revision = "e16e847cb3b8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="cascade",
    )


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
