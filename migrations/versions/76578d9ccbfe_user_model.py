"""User model

Revision ID: 76578d9ccbfe
Revises: 04d6f30432a1
Create Date: 2022-10-27 20:11:33.894118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "76578d9ccbfe"
down_revision = "04d6f30432a1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tb_user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_tb_user_email"), "tb_user", ["email"], unique=True)
    op.create_index(op.f("ix_tb_user_id"), "tb_user", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_tb_user_id"), table_name="tb_user")
    op.drop_index(op.f("ix_tb_user_email"), table_name="tb_user")
    op.drop_table("tb_user")
    # ### end Alembic commands ###
