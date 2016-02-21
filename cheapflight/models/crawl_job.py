# coding: utf-8

from datetime import datetime

from sqlalchemy import Column
import sqlalchemy.types as dbt
from sqlalchemy.schema import UniqueConstraint

from cheapflight.ext import db
from cheapflight.models.base import EntityModel


class CrawlJob(EntityModel):

    __tablename__ = 'crawl_job'

    flight_date = Column(dbt.DATE, nullable=False)
    airline = Column(dbt.CHAR(32), nullable=False)
    origin = Column(dbt.CHAR(3), nullable=False)
    destination = Column(dbt.CHAR(3), nullable=False)

    period = Column(dbt.Integer, default=24*60*60)
    next_run_after = Column(dbt.DATETIME, nullable=False, default=0)

    _unique_cols = ("flight_date", "airline", "origin", "destination")
    __table_args__ = (UniqueConstraint(*_unique_cols, name='unique_job'),)

    def __str__(self):
        return "%s %s-%s/%s every %ss" % (
            self.flight_date,
            self.origin,
            self.destination,
            self.airline,
            self.period,
        )

    @classmethod
    def upsert(cls, **data):
        # TODO testme
        id_ = cls.add(**data)
        if id_ is not None:
            return id_

        filter_cond = {
            k: v
            for k, v in data.iteritems()
            if k in set(cls._unique_cols)
        }
        matches = cls.query.filter_by(**filter_cond)
        data.pop("id", None)
        n_effected = matches.update(data)
        assert n_effected == 1
        return matches[0].id

    def to_dict(self):
        return {
            "id": self.id,
            "flight_date": self.flight_date.strftime("%Y-%m-%d"),
            "airline": self.airline,
            "origin": self.origin,
            "destination": self.destination,
            "period": self.period,
            "next_run_after": self.next_run_after.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @classmethod
    def get_jobs(cls, at=datetime.now()):
        if at is None:
            return cls.query.all()

        return cls.query.filter(
            cls.next_run_after <= at
        ).all()
