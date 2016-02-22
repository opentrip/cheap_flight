#!./venv/bin/python
# coding: utf-8
import sys
from datetime import datetime

from cheapflight.utils import iterdates
from cheapflight.constants import WEEDDAYS

from cheapflight.airlines.ha import HighAvailabilitySearcher


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


def main(argv):
    if len(argv) != 6:
        print 'usage: python this.py airasia PEK KUL 2015-10-01 2016-01-01'
        return 1

    airline = argv[1]
    dep = argv[2]  # PEK
    arr = argv[3]  # KUL
    begin_date = datetime.strptime(argv[4], "%Y-%m-%d").date()
    end_date = datetime.strptime(argv[5], "%Y-%m-%d").date()

    for date_ in iterdates(begin_date, end_date):
        price = get_lowest_price_from_remote(airline, dep, arr, date_)

        if price is None:
            continue

        print '%s (%s) %s-%s CNY: %d' % (
            date_.strftime("%Y-%m-%d"), WEEDDAYS[date_.weekday()],
            dep, arr, price,
        )


if __name__ == '__main__':
    main(sys.argv)
