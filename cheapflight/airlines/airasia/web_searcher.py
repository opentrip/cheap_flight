# coding: utf-8
from decimal import Decimal
from datetime import date
import requests

from cheapflight.libs.mc import cache
from pyquery import PyQuery as pq
from cheapflight.utils import exchange_to_cny, get_fake_ip
from .schedule import FLIGHT_SCHEDULE


MC_KEY_WEB_RESULT = ("airasia:web_result:{dep_code}:{arr_code}:"
                     "{departure_date}")


class Searcher(object):

    BASE_URL = 'https://booking.airasia.com/Flight/Select'
    BASE_HTTP_HEADER = {
        'accept': ('text/html,application/xhtml+xml,application/xml;'
                   'q=0.9,image/webp,*/*;q=0.8'),
        'accept-encoding': 'gzip, deflate, sdch',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2',
        'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/45.0.2454.93 Safari/537.36'),
    }
    AIRLINE_NAME = 'AirAsia'
    FLIGHT_SCHEDULE = set(FLIGHT_SCHEDULE)

    def __init__(self):
        self.http = requests.Session()

    @cache(MC_KEY_WEB_RESULT, 3600 * 2)
    def search(self, dep_code, arr_code, departure_date):
        return self.search_without_cache(dep_code, arr_code, departure_date)

    def search_without_cache(self, dep_code, arr_code, departure_date):
        http_headers = self.BASE_HTTP_HEADER.copy()
        http_headers['x-forwarded-for'] = get_fake_ip()
        res = self.http.get(
            self.BASE_URL,
            headers=http_headers,
            params={
                'o1': dep_code,
                'd1': arr_code,
                'dd1': departure_date.strftime("%Y-%m-%d"),
                'ADT': 1,
                'CHD': 0,
                'inl': 0,
                's': True,
                'mon': True,
                'loy': True,
                'cc': 'CNY',
            }
        )
        if res.status_code == 200:
            return res.text

        if res.status_code in (502, 504):
            return
        else:
            raise NotImplementedError(
                "Unknown code: %s\n%s" % (res.status_code, res.text)
            )

    @staticmethod
    def parse_lowest_price(html_data):
        html_dom = pq(html_data)
        fare_dom = html_dom('div.avail-fare-price')
        price_str_list = [
            price_dom.text.strip()
            for price_dom in fare_dom
        ]
        if not price_str_list:
            raise ValueError(html_dom)

        lowest_price = None
        currency_code = None
        for price_str in price_str_list:
            price_, currency_code_ = price_str.split(" ")
            if currency_code is None:
                currency_code = currency_code_
            else:
                assert currency_code == currency_code_
            price_ = Decimal(
                price_.strip(u"≈ ").replace(",", "")
            )
            if lowest_price is None or price_ < lowest_price:
                lowest_price = price_

        assert currency_code is not None

        if currency_code != 'CNY':
            lowest_price_in_cny = exchange_to_cny(currency_code, lowest_price)
        else:
            lowest_price_in_cny = lowest_price

        return lowest_price_in_cny

    def get_lowest_price(self, dep_code='PEK', arr_code='KUL',
                         departure_date=date(2016, 5, 2)):
        data = self.search(dep_code, arr_code, departure_date)
        return self.parse_lowest_price(data)


__all__ = ['Searcher']
