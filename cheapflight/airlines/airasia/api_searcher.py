# coding: utf-8

import uuid
import base64
import hashlib
import requests
from decimal import Decimal
from datetime import date, datetime, timedelta
from cheapflight.libs.mc import cache
from cheapflight.utils import get_fake_ip
from cheapflight.airlines.airasia.schedule import FLIGHT_SCHEDULE


MC_KEY_API_RESULT = ("airasia:api_result:{dep_code}:{arr_code}:"
                     "{departure_date}")
_AAE = base64.decodestring("cm9iZXJ0LmFpcmFzaWFAZ3" + "VlcnJpbGxhbWFpbC5jb20=")
_AAP = base64.decodestring("UDRabk" + "dFS3k=")
_SALT = base64.decodestring("ZjE1MmU5ZWZiZjZjZWY0YT" + "FlMmM0MmE2MWI2YjJjYjU=")
_CMP = base64.decodestring("Tmd4dGNZY" + "zVIbg==")
_DID = base64.decodestring("OTBGOEU1MkYtRjE5Qy00" + "NUZFLThFQzktREFFNTAyQTAzREFD")


class Searcher(object):

    BASE_URL = "https://ac" + "me.air" + "asia.com/api/apps.php/"
    BASE_HTTP_HEADER = {
        "user-agent": "Air" + "AsiaMobile/3.3.0 (iPhone; iOS 9.2; Scale/2.00)",
        "content-type": "application/x-www-form-urlencoded; charset=utf-8",
        "accept": "*/*",
        "authorization": "Basic Og=="
    }
    AIRLINE_NAME = "Air" + "Asia"
    FLIGHT_SCHEDULE = set(FLIGHT_SCHEDULE)
    DEVICE_ID = str(uuid.uuid4()).upper()

    def __init__(self):
        self.http = requests.Session()
        self.session = {}

    @staticmethod
    def get_hash_key(dct, salt=_SALT):
        kvs = "".join(sorted(
            ("%s=%s" % (k, v) for k, v in dct.iteritems()),
            key=lambda s: s.lower()
        ))
        hfn = hashlib.sha256()
        hfn.update(kvs + salt)
        return hfn.hexdigest()

    def _action_201(self, email=_AAE, password=_AAP):
        '''login'''
        query_params = {
            "MCC": "460",
            "MNC": "01",
            "actionCode": "201",
            "appVersion": "3.3.0",
            "countryCode": "CN",
            "cultureCode": "en-GB",
            "deviceBrand": "apple",
            "deviceID": self.DEVICE_ID,
            "deviceModel": "iPhone7,2",
            "operatingSystem": "ios",
            "osVersion": "9.2",
            "email": email,
            "password": password,
            "username": "AAM_MOBILE",
        }
        hash_key = self.get_hash_key(query_params)
        query_params["hashKey"] = hash_key

        http_headers = self.BASE_HTTP_HEADER.copy()
        http_headers["x-forwarded-for"] = get_fake_ip()
        res = self.http.post(
            self.BASE_URL,
            headers=http_headers,
            data=query_params,
        )
        if res.status_code != 200:
            raise ValueError(res.status_code)
        d = res.json()
        if d["response"]["responseCode"] != 1000:
            raise ValueError(d)

        self.session["useremail"] = email
        self.session["username"] = str(d["data"]["result"]["username"])
        self.session["sso_ticket"] = str(d["data"]["ssoTicket"])
        self.session["big_member_id"] = int(d["data"]["result"]["BigMemberID"])

    def _action_205(self):
        '''unknown confirm 1'''
        query_params = {
            "MCC": "460",
            "MNC": "01",
            "actionCode": "205",
            "appVersion": "3.3.0",
            "countryCode": "CN",
            "cultureCode": "en-GB",
            "customerId": self.session["big_member_id"],
            "deviceBrand": "apple",
            "deviceID": self.DEVICE_ID,
            "deviceModel": "iPhone7,2",
            "operatingSystem": "ios",
            "osVersion": "9.2",
            "password": _CMP,
            "ssoTicket": self.session["sso_ticket"],
            "userEmail": self.session["useremail"],
            "username": self.session["username"],
        }

        hash_key = self.get_hash_key(query_params)
        query_params["hashKey"] = hash_key

        http_headers = self.BASE_HTTP_HEADER.copy()
        http_headers["x-forwarded-for"] = get_fake_ip()
        res = self.http.post(
            self.BASE_URL,
            headers=http_headers,
            data=query_params,
        )
        if res.status_code != 200:
            raise ValueError(res.status_code)
        d = res.json()
        if d["response"]["responseCode"] != 1000:
            raise ValueError(d)

        self.session["sso_ticket"] = str(d["data"]["ssoTicket"])

    def _action_204(self):
        '''unknown confirm 2'''

        query_params = {
            "MCC": "460",
            "MNC": "01",
            "actionCode": "204",
            "appVersion": "3.3.0",
            "countryCode": "CN",
            "cultureCode": "en-GB",
            "deviceBrand": "apple",
            "deviceID": self.DEVICE_ID,
            "deviceModel": "iPhone7,2",
            "operatingSystem": "ios",
            "osVersion": "9.2",
            "password": _CMP,
            "ssoTicket": self.session["sso_ticket"],
            "userEmail": self.session["useremail"],
            "username": self.session["username"],
        }

        hash_key = self.get_hash_key(query_params)
        query_params["hashKey"] = hash_key

        http_headers = self.BASE_HTTP_HEADER.copy()
        http_headers["x-forwarded-for"] = get_fake_ip()
        res = self.http.post(
            self.BASE_URL,
            headers=http_headers,
            data=query_params,
        )
        if res.status_code != 200:
            raise ValueError(res.status_code)
        d = res.json()
        if d["response"]["responseCode"] != 1000:
            raise ValueError(d)

        self.session["sso_ticket"] = str(d["data"]["ssoTicket"])

    def _action_103(self):
        '''get query session'''
        query_params = {
            "MCC": "460",
            "MNC": "01",
            "actionCode": "103",
            "appVersion": "3.3.0",
            "countryCode": "CN",
            "cultureCode": "en-GB",
            "deviceBrand": "apple",
            "deviceID": self.DEVICE_ID,
            "deviceModel": "iPhone7,2",
            "operatingSystem": "ios",
            "osVersion": "9.2",
            "password": _CMP,
            "requestFrom": "0",
            "requestType": "1",
            "userEmail": self.session["useremail"],
            "username": "AAM_MOBILE",
        }
        hash_key = self.get_hash_key(query_params)
        query_params["hashKey"] = hash_key

        http_headers = self.BASE_HTTP_HEADER.copy()
        http_headers["x-forwarded-for"] = get_fake_ip()
        res = self.http.post(
            self.BASE_URL,
            headers=http_headers,
            data=query_params,
        )
        if res.status_code != 200:
            raise ValueError(res.status_code)
        d = res.json()
        if d["response"]["responseCode"] != 1000:
            raise ValueError(d)

        self.session["user_session"] = str(d["data"]["userSession"])

    def _action_302(self, dep_code="PEK", arr_code="KUL", departure_date=date(2016, 5, 2), ):
        ''' query '''
        query_params = {
            "MCC": "460",
            "MNC": "01",
            "actionCode": "302",
            "adultPax": "1",
            "appVersion": "3.3.0",
            "arrivalStation": arr_code,
            "childPax": "0",
            "countryCode": "CN",
            "cultureCode": "en-GB",
            "departureDate": departure_date.strftime("%Y-%m-%d"),
            "departureStation": dep_code,
            "deviceBrand": "apple",
            "deviceID": self.DEVICE_ID,
            "deviceModel": "iPhone7,2",
            "infantPax": "0",
            "operatingSystem": "ios",
            "osVersion": "9.2",
            "password": _CMP,
            "requestFrom": "0",
            "returnDate": "",
            "userCurrencyCode": "CNY",
            "userEmail": self.session["useremail"],
            "userSession": self.session["user_session"],
            "username": "AAM_MOBILE",
        }
        hash_key = self.get_hash_key(query_params)
        query_params["hashKey"] = hash_key

        http_headers = self.BASE_HTTP_HEADER.copy()
        http_headers["x-forwarded-for"] = get_fake_ip()
        res = self.http.post(
            self.BASE_URL,
            headers=http_headers,
            data=query_params,
        )
        if res.status_code != 200:
            raise ValueError(res.status_code)
        d = res.json()
        if d["response"]["responseCode"] != 1000:
            raise ValueError(d)

        if d["data"]["FlightSearch"] == [[]]:
            raise ValueError(d)

        return d["data"]

    @cache(MC_KEY_API_RESULT, 2 * 3600)
    def search(self, dep_code, arr_code, departure_date):
        return self.search_without_cache(dep_code, arr_code, departure_date)

    def search_without_cache(self, dep_code, arr_code, departure_date):
        login = self._action_201
        confirm1 = self._action_205
        confirm2 = self._action_204
        get_session = self._action_103
        query = self._action_302

        user_session = self.session.get("user_session")
        if not user_session:
            login()
            confirm1()
            confirm2()

        get_session()
        return query(dep_code, arr_code, departure_date)

    @staticmethod
    def parse_lowest_price(json_data, departure_date):
        date_key = departure_date.strftime("%Y-%m-%d")
        low_fare_dict = json_data["LowestFareArr"][0]
        currency_code = str(json_data["departureCurrencyCode"])
        exchange_rate = Decimal(json_data["exchangeRate"])
        lowest_price = Decimal(low_fare_dict[date_key])
        if currency_code != "CNY":
            lowest_price_in_cny = exchange_rate * lowest_price
        else:
            lowest_price_in_cny = lowest_price

        return lowest_price_in_cny

    def get_lowest_price(self, dep_code="PEK", arr_code="KUL",
                         departure_date=date(2016, 5, 2)):
        json_data = self.search(dep_code, arr_code, departure_date)
        return self.parse_lowest_price(json_data, departure_date)
