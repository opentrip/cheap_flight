from datetime import timedelta


def iterdates(start_date, end_date, delta=timedelta(days=1)):
    current_date= start_date
    while current_date < end_date:
        yield current_date
        current_date += delta
