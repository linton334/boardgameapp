"""initial migration

Revision ID: f13061243d98
Revises: 
Create Date: 2022-11-29 12:19:32.088815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f13061243d98'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board_game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=True),
    sa.Column('desc', sa.String(length=500), nullable=True),
    sa.Column('releaseDate', sa.Date(), nullable=True),
    sa.Column('playerCount', sa.Integer(), nullable=True),
    sa.Column('playTime', sa.Integer(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('complexity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('board_game')
    # ### end Alembic commands ###
