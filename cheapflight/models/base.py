# coding: utf-8
import time
import datetime

from simpleflake import simpleflake, parse_simpleflake
from werkzeug.utils import cached_property
import sqlalchemy
from sqlalchemy import Column, BigInteger
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.declarative import declared_attr

from cheapflight.ext import db


class EntityModel(db.Model):

    __abstract__ = True

    def __repr__(self):
        cls_name = self.__class__.__name__
        attrs = ('%s=%r' % (attr.key, attr.value)
                 for attr in inspect(self).attrs)
        joined_attrs = ', '.join(attrs)
        return '%s(%s)' % (cls_name, joined_attrs)

    @declared_attr
    def id(cls):
        return Column(BigInteger, primary_key=True, default=simpleflake)

    @declared_attr
    def updated_at_timestamp(self):
        return Column(BigInteger, default=int(time.time() + 0.5),
                      nullable=False)

    @cached_property
    def simpleflake(self):
        return parse_simpleflake(self.id)

    @cached_property
    def created_at(self):
        return datetime.datetime.fromtimestamp(self.simpleflake.timestamp)

    @cached_property
    def updated_at(self):
        return datetime.datetime.fromtimestamp(self.updated_at_timestamp)

    @classmethod
    def get(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def add(cls, **data):
        obj = cls(**data)
        db.session.add(obj)
        try:
            db.session.commit()
            return obj.id
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            return None

    def update(self, **data):
        data.pop('id', None)
        data['updated_at_timestamp'] = int(time.time() + 0.5)
        ret = self.__class__.query.filter_by(id=self.id).update(data)
        db.session.commit()
        return ret

    @classmethod
    def delete(cls, id_):
        return cls.query.filter_by(id=id_).delete()
