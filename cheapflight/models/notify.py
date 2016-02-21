# coding: utf-8

from datetime import datetime


def on_price_change(flight_date, origin, destination,
                    airline, price, now_ts, existed):
    # TODO subscribe and email
    dt = datetime.fromtimestamp(now_ts)
    print "[%s] %s @%s %s-%s %+.2f CNY" % (
        dt.strftime("%Y-%m-%d %H:%M:%S"),
        flight_date, airline, origin, destination, price - existed.price_cny
    )
