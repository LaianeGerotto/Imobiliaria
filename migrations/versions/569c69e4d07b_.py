"""empty message

Revision ID: 569c69e4d07b
Revises: 47be2b1ce23f
Create Date: 2022-04-18 19:47:27.992762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '569c69e4d07b'
down_revision = '47be2b1ce23f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('senha', sa.String(length=100), nullable=True),
    sa.Column('nome', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usuario')
    # ### end Alembic commands ###
