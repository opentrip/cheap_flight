# coding: utf-8

import time
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy import Column
import sqlalchemy.types as dbt
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.schema import UniqueConstraint

from cheapflight.models.base import EntityModel


class CrawlJob(EntityModel):

    __tablename__ = 'crawl_job'

    flight_date = Column(dbt.DATE, nullable=False)
    airline = Column(dbt.CHAR(32), nullable=False)
    origin = Column(dbt.CHAR(3), nullable=False)
    destination = Column(dbt.CHAR(3), nullable=False)

    next_run_after = Column(sa.BigInteger, nullable=False, default=0)

    UniqueConstraint("flight_date", "airline", "origin", "destination", name='unique_job')
