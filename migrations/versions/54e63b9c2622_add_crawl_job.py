"""add crawl_job

Revision ID: 54e63b9c2622
Revises: 28365ba8c39e
Create Date: 2016-01-13 00:19:35.268309

"""

# revision identifiers, used by Alembic.
revision = '54e63b9c2622'
down_revision = '28365ba8c39e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'crawl_job',
        sa.Column('flight_date', sa.DATE(), nullable=False),
        sa.Column('airline', sa.CHAR(length=32), nullable=False),
        sa.Column('origin', sa.CHAR(length=3), nullable=False),
        sa.Column('destination', sa.CHAR(length=3), nullable=False),
        sa.Column('next_run_after', sa.BigInteger(), nullable=False),
        sa.Column('updated_at_timestamp', sa.BigInteger(), nullable=False),
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('crawl_job')
