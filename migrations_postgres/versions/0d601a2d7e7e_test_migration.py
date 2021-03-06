"""test_migration

Revision ID: 0d601a2d7e7e
Revises: 47ff5284e01f
Create Date: 2021-09-10 00:28:52.238371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d601a2d7e7e'
down_revision = '47ff5284e01f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Test',
    sa.Column('created_by', sa.String(length=255), nullable=False),
    sa.Column('created_date', sa.Text(), nullable=True),
    sa.Column('edited_by', sa.String(length=255), nullable=True),
    sa.Column('edited_date', sa.Text(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Test')
    # ### end Alembic commands ###
