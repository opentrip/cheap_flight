import urllib
import requests
from decimal import Decimal
from datetime import date
from cheap_flight.libs.mc import cache
from cheap_flight.utils import exchange_to_cny, get_fake_ip
from .schedule import FLIGHT_SCHEDULE


class Searcher(object):

    BASE_URL = ('https://cebu-booking.ink-global.com'
                '/api/tenants/cebu/availability;ADT=1')
    BASE_HEADER_KEY, BASE_HEADER_VALUE = urllib.quote(BASE_URL, safe="=").split("=")
    BASE_HTTP_HEADER = {
        'content-type': 'application/vnd.inkglobal.flights.v1+json',
        'accept': ('application/json,'
                   'application/vnd.inkglobal.flights.v1+json,'
                   'application/vnd.inkglobal.flights.v1+json'),
        'user-agent': 'iPhone,iPhone',
        'accept-language': 'zh-cn',
        'x-forwarded-for': get_fake_ip(),
        BASE_HEADER_KEY: BASE_HEADER_VALUE
    }
    AIRLINE_NAME = 'CebuPacific'
    FLIGHT_SCHEDULE = set(FLIGHT_SCHEDULE)

    def __init__(self):
        self.http = requests.Session()

    def __del__(self):
        self.http.close()

    @cache("price:cebu_pacific:{dep_code}:{arr_code}:{departure_date}")
    def search(self, dep_code, arr_code, departure_date):
        res = self.http.get(
            self.BASE_URL,
            headers=self.BASE_HTTP_HEADER,
            params={
                'from': dep_code,
                'to': arr_code,
                'departureDate': departure_date.strftime("%Y-%m-%d"),
            }
        )
        return res.json()

    @staticmethod
    def parse_lowest_price(json_data):
        price_list = []
        currency_code = None
        for flight in json_data['outbound']:
            for seat in flight['prices']:
                price = seat['price']
                if currency_code is None:
                    currency_code = price['currencyCode']
                else:
                    assert currency_code == price['currencyCode']
                price_list.append(Decimal(price['value']))
        if not price_list:
            return None

        lowest_price = min(price_list)
        if currency_code != 'CNY':
            lowest_price_in_cny = exchange_to_cny(currency_code, lowest_price)
        else:
            lowest_price_in_cny = lowest_price
        return lowest_price_in_cny

    def get_lowest_price(self, dep_code='PEK', arr_code='MNL',
                         departure_date=date(2016, 5, 2)):
        json_data = self.search(dep_code, arr_code, departure_date)
        return self.parse_lowest_price(json_data)
