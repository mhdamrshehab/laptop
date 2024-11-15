"""Add Product tables

Revision ID: 433feebcf44f
Revises: 94b496eff2b5
Create Date: 2024-10-15 14:20:00.324447

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '433feebcf44f'
down_revision = '94b496eff2b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=False))
        batch_op.drop_column('items_number')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('items_number', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###
