import requests
from decimal import Decimal
from cheapflight.libs.mc import mc


def exchange_currency(from_currency, from_amount,
                      to_currency='CNY',
                      base_currency='USD'):
    key = "exchange_rate:from:%s:to:%s:based_on:%s" % (
        from_currency, to_currency, base_currency
    )
    cached = mc.get(key)
    if cached is None:
        cached = requests.get(
            'http://api.fixer.io/latest',
            params={
                'base': base_currency,
                'symbols': ','.join([from_currency, to_currency])
            }
        ).json()
        mc.set(key, cached)
    rates = cached['rates']
    rate = Decimal(rates[to_currency]) / Decimal(rates[from_currency])
    return rate * from_amount


def exchange_to_cny(from_currency, from_amount):
    if not isinstance(from_amount, Decimal):
        from_amount = Decimal(from_amount)
    return exchange_currency(
        from_currency, from_amount,
        to_currency='CNY', base_currency='USD'
    )


def main():
    print exchange_currency('PHP', 1)


if __name__ == '__main__':
    main()
