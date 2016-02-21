# coding: utf-8
import time
from datetime import datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy import Column
import sqlalchemy.types as dbt

from cheapflight.models.base import EntityModel
from cheapflight.models.notify import on_price_change


class LowestPriceHistory(EntityModel):
    '''
    CZ3997:xx(a)n(n)(n)(n)(a)
        https://en.wikipedia.org/wiki/Airline_codes
    PEK:aaa
        https://en.wikipedia.org/wiki/International_Air_Transport_Association_airport_code
    '''

    __tablename__ = 'lowest_price_history'
    flight_date = Column(dbt.DATE, nullable=False)
    origin = Column(dbt.CHAR(3), nullable=False)
    destination = Column(dbt.CHAR(3), nullable=False)

    airline = Column(dbt.CHAR(32), nullable=False)
    price_cny = Column(dbt.DECIMAL(8, 2), nullable=False)
    first_seen_at = Column(sa.BigInteger, nullable=False)
    last_seen_at = Column(sa.BigInteger, nullable=False)

    @classmethod
    def add(cls, flight_date, origin, destination, airline, price_cny,
            first_seen_at=time.time()):

        payload = {
            'flight_date': flight_date,
            'origin': origin,
            'destination': destination,
            'airline': airline,
            'price_cny': price_cny,
            'first_seen_at': first_seen_at,
            'last_seen_at': first_seen_at,
        }
        return super(LowestPriceHistory, cls).add(**payload)

    def to_dict(self):
        return {
            'flight_date': self.flight_date.strftime("%Y-%m-%d"),
            'origin': self.origin,
            'destination': self.destination,
            'airline': self.airline,
            'price_cny': float(self.price_cny),
            'first_seen_at': datetime.fromtimestamp(self.first_seen_at),
            'last_seen_at': datetime.fromtimestamp(self.first_seen_at),
        }

    @classmethod
    def get_latest_price(cls, flight_date, origin, destination):
        return cls.query.filter_by(
            flight_date=flight_date,
            origin=origin,
            destination=destination,
        ).order_by(
            sa.desc(cls.last_seen_at)
        ).first()

    @classmethod
    def list(cls):
        price_dict = {}
        for rec in cls.query.all():
            price_dict.setdefault(
                (rec.flight_date, rec.origin, rec.destination),
                []
            ).append(
                (rec.id, rec.airline, rec.first_seen_at, rec.last_seen_at,
                 rec.price_cny)
            )

        price_list = []
        for unique_record, history in price_dict.iteritems():
            flight_date, origin, destination = unique_record
            price_list.append({
                'flight_date': flight_date.strftime("%Y-%m-%d"),
                'origin': origin,
                'destination': destination,
                'priceline': [
                    {
                        'id': str(id_),
                        'airline': airline,
                        'price_cny': float(price_cny),
                        'first_seen_at': datetime.fromtimestamp(first_seen_at).strftime("%Y-%m-%d %H:%M:%S"),
                        'last_seen_at': datetime.fromtimestamp(last_seen_at).strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    for (id_, airline, first_seen_at, last_seen_at, price_cny)
                    in sorted(history, key=lambda x: x[3])
                ],
            })
        return price_list

    @classmethod
    def update_price(cls, flight_date, origin, destination, price, airline,
                     now_ts=time.time()):
        if not isinstance(price, Decimal):
            raise ValueError("price should be of type decimal.Decimal")

        existed = cls.get_latest_price(flight_date, origin, destination)
        if existed is None:
            return cls.add(
                flight_date, origin, destination, airline, price, now_ts
            )

        if abs(existed.price_cny - price) > 0.01:
            on_price_change(flight_date, origin, destination,
                            airline, price, now_ts, existed)
            return cls.add(
                flight_date, origin, destination, airline, price, now_ts
            )

        payload = {
            'last_seen_at': now_ts
        }
        if existed.airline != airline:
            payload['airline'] = airline

        existed.update(**payload)
        return existed.id
