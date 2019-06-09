"""empty message

Revision ID: f9829baa1eec
Revises: 06373aa29ffe
Create Date: 2019-03-08 20:28:19.870380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9829baa1eec'
down_revision = '06373aa29ffe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('firstName', sa.String(length=128), nullable=False))
    op.add_column('users', sa.Column('lastName', sa.String(length=128), nullable=False))
    op.add_column('users', sa.Column('password', sa.String(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    op.drop_column('users', 'lastName')
    op.drop_column('users', 'firstName')
    # ### end Alembic commands ###
