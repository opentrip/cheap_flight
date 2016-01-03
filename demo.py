#!./venv/bin/python
# coding: utf-8
import sys
from cheapflight import create_app

from cheapflight.utils import iterdates
from cheapflight.constants import WEEDDAYS
from cheapflight.models.rader import fetch_and_store
from datetime import datetime


def main(argv):
    if len(argv) != 5:
        print 'usage: python this.py PEK KUL 2015-10-01 2016-01-01'
        return 1

    dep = argv[1]  # PEK
    arr = argv[2]  # KUL
    begin_date = datetime.strptime(argv[3], "%Y-%m-%d").date()
    end_date = datetime.strptime(argv[4], "%Y-%m-%d").date()

    for date_ in iterdates(begin_date, end_date):
        price = fetch_and_store(dep, arr, date_)

        if price is None:
            continue

        print '%s (%s) %s-%s CNY: %d' % (
            date_.strftime("%Y-%m-%d"), WEEDDAYS[date_.weekday()],
            dep, arr, price,
        )


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        sys.exit(main(sys.argv))
