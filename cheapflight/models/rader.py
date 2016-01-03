# coding: utf-8
import time
from cheapflight.airlines.ha import HighAvailabilitySearcher
from cheapflight.models.price_history import LowestPriceHistory


available_airlines = [
    'airasia',
    'cebupacific'
]


def get_available_airlines(dep_code, arr_code, departure_date):
    aa = []
    for airline in available_airlines:
        flight_schedule = __import__(
            "cheapflight.airlines.%s.schedule" % airline,
            fromlist=['FLIGHT_SCHEDULE']
        )
        if (dep_code, arr_code) in flight_schedule.FLIGHT_SCHEDULE:
            aa.append(airline)
    return aa


def get_lowest_price_from_remote(airline, dep_code, arr_code, departure_date):
    mod = __import__(
        "cheapflight.airlines.%s" % airline,
        fromlist=['Searcher']
    )
    if isinstance(mod.Searcher, (list, tuple)):
        searcher = HighAvailabilitySearcher([mt() for mt in mod.Searcher])
    else:
        searcher = mod.Searcher()

    return searcher.get_lowest_price(dep_code, arr_code, departure_date)


def fetch_and_store(dep_code, arr_code, departure_date,
                    cache_expiration=6*3600):
    latest_price = LowestPriceHistory.get_latest_price(
        departure_date, dep_code, arr_code
    )
    if latest_price:
        if time.time() - latest_price.last_seen_at < cache_expiration:
            return latest_price.price_cny

    price_list = []
    for airline in get_available_airlines(dep_code, arr_code, departure_date):
        price = get_lowest_price_from_remote(
            airline, dep_code, arr_code, departure_date
        )
        if price is None:
            continue
        LowestPriceHistory.update_price(
            departure_date, dep_code, arr_code, price, airline
        )
        price_list.append(price)
    lowest_price = min(price_list) if price_list else None
    return lowest_price
