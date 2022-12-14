"""Added access code column to user

Revision ID: 683b60688f98
Revises: f852e8e7c1eb
Create Date: 2022-11-15 17:45:58.277113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '683b60688f98'
down_revision = 'f852e8e7c1eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('alpaca_access_code', sa.String(length=40), nullable=True))
    op.create_index(op.f('ix_user_alpaca_access_code'), 'user', ['alpaca_access_code'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_alpaca_access_code'), table_name='user')
    op.drop_column('user', 'alpaca_access_code')
    # ### end Alembic commands ###
