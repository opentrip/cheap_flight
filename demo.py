#!./venv/bin/python
# coding: utf-8
import sys
from cheap_flight.utils import iterdates
from cheap_flight.constants import WEEDDAYS
from datetime import datetime


available_airlines = [
    'airasia',
    'cebupacific'
]

def iter_searchers():
    for airline in available_airlines:
        mod  = __import__(
            "cheap_flight.airlines.%s" % airline,
            fromlist=['Searcher']
        )
        yield mod.Searcher()


def main(argv):
    if len(argv) != 5:
        print 'usage: python this.py PEK KUL 2015-10-01 2016-01-01'
        return 1

    dep = argv[1]  # PEK
    arr = argv[2]  # KUL
    begin_date = datetime.strptime(argv[3], "%Y-%m-%d").date()
    end_date = datetime.strptime(argv[4], "%Y-%m-%d").date()

    for date_ in iterdates(begin_date, end_date):

        for searcher in iter_searchers():
            if (dep, arr) not in searcher.FLIGHT_SCHEDULE:
                continue

            price = searcher.get_lowest_price(dep, arr, date_)

            if price is None:
                continue

            print '%s (%s) %s-%s CNY: %d (%s)' % (
                date_.strftime("%Y-%m-%d"), WEEDDAYS[date_.weekday()],
                dep, arr, price, searcher.AIRLINE_NAME
            )


if __name__ == '__main__':
    sys.exit(main(sys.argv))
