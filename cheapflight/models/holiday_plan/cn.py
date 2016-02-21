# coding: utf-8

from datetime import datetime, date, timedelta
from cheapflight.utils import iterdates

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7)


def _strtodate(day):
    return datetime.strptime(day, "%Y-%m-%d").date()


# 调休上班
SPEC_WORKDAYS = [_strtodate(day) for day in (
    "2016-02-06",
    "2016-02-14",
    "2016-06-12",
    "2016-09-18",
    "2016-10-08",
    "2016-10-09",
)]

# 假期
SPEC_HOLIDAYS = [_strtodate(day) for day in (
    "2016-01-01",
    "2016-02-08",
    "2016-02-09",
    "2016-02-10",
    "2016-02-11",
    "2016-02-12",
    "2016-04-04",
    "2016-05-02",
    "2016-06-09",
    "2016-06-10",
    "2016-09-15",
    "2016-09-16",
    "2016-10-03",
    "2016-10-04",
    "2016-10-05",
    "2016-10-06",
    "2016-10-07",
)]


def validate():
    print "调休上班: %d" % len(SPEC_WORKDAYS)
    print "假期: %d" % len(SPEC_HOLIDAYS)

    for day in SPEC_WORKDAYS:
        assert day.weekday() in {SATURDAY, SUNDAY}, (
            "%s本来就是工作日，无需放入特殊工作日列表" % day
        )

    for day in SPEC_HOLIDAYS:
        assert day.weekday() not in {SATURDAY, SUNDAY}, (
            "%s本来就是休息日，无需放入特殊休息日列表" % day
        )


def is_holiday(day):
    if day in SPEC_WORKDAYS:
        return False
    if day in SPEC_HOLIDAYS:
        return True
    return day.weekday() in {SATURDAY, SUNDAY}


def main():
    today = date(2016, 1, 1)  # date.today()
    plan_period = timedelta(days=365)
    min_travel_days = 3
    for start_day in iterdates(today, today + plan_period):
        for travel_days in range(min_travel_days, 30):
            end_date = start_day + timedelta(days=travel_days + 1)
            if is_holiday(end_date - timedelta(days=1)) and \
                    is_holiday(end_date):
                continue

            travel_days = list(iterdates(start_day, end_date))
            holiday_count = sum((1 for day in travel_days if is_holiday(day)))
            workday_count = len(travel_days) - holiday_count
            if workday_count > holiday_count:
                continue
            if holiday_count > workday_count:
                print "[%s, %s] 请%d天休%d天 (%.2f %%)" % (
                    start_day,
                    end_date - timedelta(days=1),
                    workday_count,
                    (workday_count + holiday_count),
                    (100.0 * workday_count / (workday_count + holiday_count))
                )


if __name__ == '__main__':
    validate()
