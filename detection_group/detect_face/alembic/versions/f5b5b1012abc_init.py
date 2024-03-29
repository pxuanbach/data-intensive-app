"""init

Revision ID: f5b5b1012abc
Revises: 
Create Date: 2023-02-02 00:44:34.510846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5b5b1012abc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('detect_body',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('img_id', sa.Integer(), nullable=True),
    sa.Column('x', sa.Float(), nullable=True),
    sa.Column('y', sa.Float(), nullable=True),
    sa.Column('width_of_obj', sa.Float(), nullable=True),
    sa.Column('height_of_obj', sa.Float(), nullable=True),
    sa.Column('width_of_img', sa.Float(), nullable=True),
    sa.Column('height_of_img', sa.Float(), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_detect_body_id'), 'detect_body', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_detect_body_id'), table_name='detect_body')
    op.drop_table('detect_body')
    # ### end Alembic commands ###
