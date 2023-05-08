"""empty message

Revision ID: 47d445fcceca
Revises: 3b03afaa6560
Create Date: 2023-04-13 21:14:50.349338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47d445fcceca'
down_revision = '3b03afaa6560'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('singnature', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('singnature')

    # ### end Alembic commands ###
