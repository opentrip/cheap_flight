# coding: utf-8

import uuid
import requests
from decimal import Decimal
from datetime import date
from cheapflight.libs.mc import cache
from cheapflight.utils import exchange_to_cny, get_fake_ip
from .schedule import FLIGHT_SCHEDULE


MC_KEY_API_RESULT = ("airasia:api_result:{dep_code}:{arr_code}:"
                     "{departure_date}")


class Searcher(object):

    BASE_URL = ('https://argon.airasia.com'
                '/api/7.0/search')
    BASE_HTTP_HEADER = {
        'channel-platform': 'iOS',
        'channel-version': '2.15.2',
        'channel': 'mobile-touch-app',
        'channel-device-uuid': str(uuid.uuid1()).upper(),
        'channel-motion': 'true',
        'channel-sim-number': 'null',
        'origin': 'file://',
        'user-agent': ('Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) '
                       'AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H143 '
                       '(5902455408)'),
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': '*/*',
    }
    AIRLINE_NAME = 'AirAsia'
    FLIGHT_SCHEDULE = set(FLIGHT_SCHEDULE)

    def __init__(self):
        self.http = requests.Session()

    def __del__(self):
        self.http.close()

    @cache(MC_KEY_API_RESULT)
    def search(self, dep_code, arr_code, departure_date):
        http_headers = self.BASE_HTTP_HEADER.copy()
        http_headers['x-forwarded-for'] = get_fake_ip()

        res = self.http.post(
            self.BASE_URL,
            headers=http_headers,
            data={
                'type': 'classic',
                'origin': dep_code,
                'destination': arr_code,
                'depart': departure_date.strftime("%d-%m-%Y"),
                'return': '',
                'passenger-count': 1,
                'child-count': 0,
                'infant-count': 0,
                'currency': 'CNY',
                'days': 1,  # ?
                'promo-code': '',  # ?
            }
        )
        if res.status_code == 200:
            return res.json()

        if res.status_code in (502, 504):
            return
        else:
            raise NotImplementedError(
                "Unknown code: %s\n%s" % (res.status_code, res.text)
            )

    @staticmethod
    def parse_lowest_price(json_data):
        if 'error' in json_data:
            return

        dates = json_data['depart']
        assert len(dates) == 1
        flight = dates.values()[0]
        if flight['lowest-price'] is None:
            return

        lowest_price = Decimal(flight['lowest-price'])
        currency_code = flight['currency']
        if currency_code != 'CNY':
            lowest_price_in_cny = exchange_to_cny(currency_code, lowest_price)
        else:
            lowest_price_in_cny = lowest_price

        return lowest_price_in_cny

    def get_lowest_price(self, dep_code='PEK', arr_code='KUL',
                         departure_date=date(2016, 5, 2)):
        json_data = self.search(dep_code, arr_code, departure_date)
        return self.parse_lowest_price(json_data)
