"""added_baseModel_for_audit

Revision ID: 931e489bc0ed
Revises: 0d601a2d7e7e
Create Date: 2021-09-10 00:35:04.496914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '931e489bc0ed'
down_revision = '0d601a2d7e7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Category', sa.Column('created_by', sa.String(length=255), nullable=False))
    op.add_column('Category', sa.Column('created_date', sa.DateTime(), nullable=False))
    op.add_column('Category', sa.Column('edited_by', sa.String(length=255), nullable=False))
    op.add_column('Category', sa.Column('edited_date', sa.DateTime(), nullable=False))
    op.add_column('ConfigTemplate', sa.Column('created_by', sa.String(length=255), nullable=False))
    op.add_column('ConfigTemplate', sa.Column('created_date', sa.DateTime(), nullable=False))
    op.add_column('ConfigTemplate', sa.Column('edited_by', sa.String(length=255), nullable=False))
    op.add_column('ConfigTemplate', sa.Column('edited_date', sa.DateTime(), nullable=False))
    op.add_column('ConfigTemplateMetadata', sa.Column('created_by', sa.String(length=255), nullable=False))
    op.add_column('ConfigTemplateMetadata', sa.Column('created_date', sa.DateTime(), nullable=False))
    op.add_column('ConfigTemplateMetadata', sa.Column('edited_by', sa.String(length=255), nullable=False))
    op.add_column('ConfigTemplateMetadata', sa.Column('edited_date', sa.DateTime(), nullable=False))
    op.add_column('Dcoument', sa.Column('created_by', sa.String(length=255), nullable=False))
    op.add_column('Dcoument', sa.Column('created_date', sa.DateTime(), nullable=False))
    op.add_column('Dcoument', sa.Column('edited_by', sa.String(length=255), nullable=False))
    op.add_column('Dcoument', sa.Column('edited_date', sa.DateTime(), nullable=False))
    op.alter_column('Test', 'created_date',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('Test', 'edited_by',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('Test', 'edited_date',
               existing_type=sa.TEXT(),
               nullable=False)
    op.add_column('role', sa.Column('created_by', sa.String(length=255), nullable=False))
    op.add_column('role', sa.Column('created_date', sa.DateTime(), nullable=False))
    op.add_column('role', sa.Column('edited_by', sa.String(length=255), nullable=False))
    op.add_column('role', sa.Column('edited_date', sa.DateTime(), nullable=False))
    op.add_column('student', sa.Column('created_by', sa.String(length=255), nullable=False))
    op.add_column('student', sa.Column('created_date', sa.DateTime(), nullable=False))
    op.add_column('student', sa.Column('edited_by', sa.String(length=255), nullable=False))
    op.add_column('student', sa.Column('edited_date', sa.DateTime(), nullable=False))
    op.add_column('user', sa.Column('created_by', sa.String(length=255), nullable=False))
    op.add_column('user', sa.Column('created_date', sa.DateTime(), nullable=False))
    op.add_column('user', sa.Column('edited_by', sa.String(length=255), nullable=False))
    op.add_column('user', sa.Column('edited_date', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'edited_date')
    op.drop_column('user', 'edited_by')
    op.drop_column('user', 'created_date')
    op.drop_column('user', 'created_by')
    op.drop_column('student', 'edited_date')
    op.drop_column('student', 'edited_by')
    op.drop_column('student', 'created_date')
    op.drop_column('student', 'created_by')
    op.drop_column('role', 'edited_date')
    op.drop_column('role', 'edited_by')
    op.drop_column('role', 'created_date')
    op.drop_column('role', 'created_by')
    op.alter_column('Test', 'edited_date',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('Test', 'edited_by',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('Test', 'created_date',
               existing_type=sa.TEXT(),
               nullable=True)
    op.drop_column('Dcoument', 'edited_date')
    op.drop_column('Dcoument', 'edited_by')
    op.drop_column('Dcoument', 'created_date')
    op.drop_column('Dcoument', 'created_by')
    op.drop_column('ConfigTemplateMetadata', 'edited_date')
    op.drop_column('ConfigTemplateMetadata', 'edited_by')
    op.drop_column('ConfigTemplateMetadata', 'created_date')
    op.drop_column('ConfigTemplateMetadata', 'created_by')
    op.drop_column('ConfigTemplate', 'edited_date')
    op.drop_column('ConfigTemplate', 'edited_by')
    op.drop_column('ConfigTemplate', 'created_date')
    op.drop_column('ConfigTemplate', 'created_by')
    op.drop_column('Category', 'edited_date')
    op.drop_column('Category', 'edited_by')
    op.drop_column('Category', 'created_date')
    op.drop_column('Category', 'created_by')
    # ### end Alembic commands ###
