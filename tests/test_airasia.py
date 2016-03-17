# coding: utf-8
import unittest
from datetime import date

from cheapflight.airlines.airasia import WebSearcher, APISearcher


class AirAsiaTestCase(unittest.TestCase):

    def setUp(self):
        self.web_searcher = WebSearcher()
        self.api_searcher = APISearcher()

    def test_web_roundtrip(self):
        html_code = self.web_searcher.search_without_cache(
            "PEK", "KUL", date(2016, 10, 1),
            date(2016, 10, 8)
        ).encode("utf-8")
        assert html_code.count(' avail-table"') == 2
        assert '<div class="avail-fare-price">' in html_code

    def test_web_outbound(self):
        html_code = self.web_searcher.search_without_cache(
            "PEK", "KUL", date(2016, 10, 1)
        ).encode("utf-8")
        assert html_code.count(' avail-table"') == 1
        assert '<div class="avail-fare-price">' in html_code

    def test_api_roundtrip(self):
        resp_json = self.api_searcher.search_without_cache(
            "PEK", "KUL", date(2016, 10, 1),
            date(2016, 10, 8)
        )
        assert "LowestFareArr" in resp_json
        assert len(resp_json["LowestFareArr"]) == 2

    def test_api_outbound(self):
        resp_json = self.api_searcher.search_without_cache(
            "PEK", "KUL", date(2016, 10, 1)
        )
        assert "LowestFareArr" in resp_json
        assert len(resp_json["LowestFareArr"]) == 1


if __name__ == '__main__':
    unittest.main()
