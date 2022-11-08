"""news_settings table

Revision ID: f852e8e7c1eb
Revises: 1cf42b66d1b0
Create Date: 2022-11-07 10:55:56.608560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f852e8e7c1eb'
down_revision = '1cf42b66d1b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('news', sa.Boolean(), nullable=False),
    sa.Column('sports', sa.Boolean(), nullable=False),
    sa.Column('tech', sa.Boolean(), nullable=False),
    sa.Column('world', sa.Boolean(), nullable=False),
    sa.Column('finance', sa.Boolean(), nullable=False),
    sa.Column('politics', sa.Boolean(), nullable=False),
    sa.Column('business', sa.Boolean(), nullable=False),
    sa.Column('economics', sa.Boolean(), nullable=False),
    sa.Column('entertainment', sa.Boolean(), nullable=False),
    sa.Column('beauty', sa.Boolean(), nullable=False),
    sa.Column('travel', sa.Boolean(), nullable=False),
    sa.Column('music', sa.Boolean(), nullable=False),
    sa.Column('food', sa.Boolean(), nullable=False),
    sa.Column('science', sa.Boolean(), nullable=False),
    sa.Column('gaming', sa.Boolean(), nullable=False),
    sa.Column('energy', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('news_settings')
    # ### end Alembic commands ###
