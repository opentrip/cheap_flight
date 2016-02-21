# coding: utf-8

import time
from datetime import date
from decimal import Decimal

from base_test_case import BaseTestCase
from cheapflight.models.price_history import LowestPriceHistory


class LowestPriceHistoryTestCase(BaseTestCase):

    def test_add_dup(self):
        flight_date = date(2016, 10, 1)
        origin = "PEK"
        destination = "KUL"
        airline = "airasia"
        now_ts = int(time.time())

        ts1 = now_ts - 1000
        rec_id1 = LowestPriceHistory.update_price(
            flight_date, origin, destination, Decimal("1024.25"), airline,
            ts1
        )
        p = LowestPriceHistory.get_latest_price(
            flight_date, origin, destination
        )
        assert p.price_cny == Decimal("1024.25")
        assert p.first_seen_at == p.last_seen_at == ts1

        ts2 = now_ts - 500
        rec_id2 = LowestPriceHistory.update_price(
            flight_date, origin, destination, Decimal("1024.25"), airline,
            ts2
        )
        assert rec_id1 == rec_id2

        p2 = LowestPriceHistory.get_latest_price(
            flight_date, origin, destination
        )

        assert p2.price_cny == Decimal("1024.25")
        assert p2.first_seen_at == ts1
        assert p2.last_seen_at == ts2
