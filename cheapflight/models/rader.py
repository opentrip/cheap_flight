# coding: utf-8
import time
from cheapflight.airlines.ha import HighAvailabilitySearcher
from cheapflight.models.price_history import LowestPriceHistory


def get_lowest_price_from_remote(airline, dep_code, arr_code, departure_date):
    mod = __import__(
        "cheapflight.airlines.%s" % airline,
        fromlist=['Searcher']
    )
    if isinstance(mod.Searcher, (list, tuple)):
        searcher = HighAvailabilitySearcher([mt() for mt in mod.Searcher])
    else:
        searcher = mod.Searcher()
    for retry in range(2):
        try:
            return searcher.get_lowest_price(
                dep_code, arr_code, departure_date
            )
        except ValueError:
            print "ValueError in %s" % searcher
    else:
        raise


def fetch_lowest_price(airline, dep_code, arr_code, departure_date,
                       cache_expiration):
    latest_price = LowestPriceHistory.get_latest_price(
        departure_date, dep_code, arr_code
    )
    if latest_price:
        if time.time() - latest_price.last_seen_at < cache_expiration:
            return latest_price.price_cny

    price = get_lowest_price_from_remote(
        airline, dep_code, arr_code, departure_date
    )
    if price is None:
        return
    LowestPriceHistory.update_price(
        departure_date, dep_code, arr_code, price, airline
    )
    return price
