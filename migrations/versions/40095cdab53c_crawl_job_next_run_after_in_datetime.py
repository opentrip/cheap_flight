"""crawl_job_next_run_after_in_datetime

Revision ID: 40095cdab53c
Revises: 54e63b9c2622
Create Date: 2016-01-31 20:49:14.077616

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '40095cdab53c'
down_revision = '54e63b9c2622'


def upgrade():
    try:
        op.drop_table("crawl_job")
    except sa.exc.OperationalError:
        pass

    op.create_table(
        'crawl_job',
        sa.Column('flight_date', sa.DATE(), nullable=False),
        sa.Column('airline', sa.CHAR(length=32), nullable=False),
        sa.Column('origin', sa.CHAR(length=3), nullable=False),
        sa.Column('destination', sa.CHAR(length=3), nullable=False),
        sa.Column('period', sa.Integer, default=24*60*60),
        sa.Column('next_run_after', sa.DATETIME, nullable=False),
        sa.Column('updated_at_timestamp', sa.DATETIME, nullable=False),
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            "flight_date", "airline", "origin", "destination",
            name="unique_job"
        )
    )


def downgrade():
    try:
        op.drop_table("crawl_job")
    except sa.exc.OperationalError:
        pass
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
