"""Create Set model

Revision ID: f56c3d2e4ec0
Revises: 3c1590ccb769
Create Date: 2022-11-02 10:41:10.958129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f56c3d2e4ec0"
down_revision = "3c1590ccb769"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tb_set",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["tb_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tb_set_id"), "tb_set", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_tb_set_id"), table_name="tb_set")
    op.drop_table("tb_set")
    # ### end Alembic commands ###
