# coding: utf-8
import json
import unittest
from datetime import date

from cheapflight.airlines.airasia import WebSearcher, APISearcher


class AirAsiaTestCase(unittest.TestCase):

    def setUp(self):
        self.web_searcher = WebSearcher()
        self.api_searcher = APISearcher()

    def test_web(self):
        html_code = self.web_searcher.search_without_cache("PEK", "KUL", date(2016, 10, 1))
        assert '<div class="avail-fare-price">' in html_code

    def test_api(self):
        resp_json = self.api_searcher.search_without_cache("PEK", "KUL", date(2016, 10, 1))
        assert "LowestFareArr" in resp_json


if __name__ == '__main__':
    unittest.main()
