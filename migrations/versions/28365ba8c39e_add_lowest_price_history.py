"""add lowest_price_history

Revision ID: 28365ba8c39e
Revises: None
Create Date: 2016-01-13 00:14:46.060079

"""

# revision identifiers, used by Alembic.
revision = '28365ba8c39e'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'lowest_price_history',
        sa.Column('flight_date', sa.DATE(), nullable=False),
        sa.Column('origin', sa.CHAR(length=3), nullable=False),
        sa.Column('destination', sa.CHAR(length=3), nullable=False),
        sa.Column('airline', sa.CHAR(length=32), nullable=False),
        sa.Column('price_cny', sa.DECIMAL(precision=8, scale=2), nullable=False),
        sa.Column('first_seen_at', sa.BigInteger(), nullable=False),
        sa.Column('last_seen_at', sa.BigInteger(), nullable=False),
        sa.Column('updated_at_timestamp', sa.BigInteger(), nullable=False),
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('lowest_price_history')
