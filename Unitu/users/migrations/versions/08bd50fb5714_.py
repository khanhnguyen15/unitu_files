"""empty message

Revision ID: 08bd50fb5714
Revises: f9829baa1eec
Create Date: 2019-03-08 21:00:21.413403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08bd50fb5714'
down_revision = 'f9829baa1eec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('isActive', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'isActive')
    # ### end Alembic commands ###
