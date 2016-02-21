# coding: utf-8

from datetime import date, timedelta

from cheapflight.utils import iterdates
from cheapflight.app import create_app
from cheapflight.models.crawl_job import CrawlJob


def generate_schedule(depart_date, arrival_date, route_list, refresh_period, days_offset=3):

    d0_range = iterdates(
        depart_date - timedelta(days=days_offset),
        depart_date + timedelta(days=days_offset + 1),
    )

    d1_range = iterdates(
        arrival_date - timedelta(days=days_offset),
        arrival_date + timedelta(days=days_offset + 1),
    )

    for d0 in d0_range:
        for airline, (ap0, ap1) in route_list:
            yield (d0, airline, ap0, ap1, refresh_period)

    for d1 in d1_range:
        for airline, (ap0, ap1) in route_list:
            yield (d1, airline, ap1, ap0, refresh_period)


def main():
    app = create_app()
    with app.app_context():

        schedule = generate_schedule(
            date(2016, 10, 1),
            date(2016, 10, 7),
            [("cebupacific", ("PEK", "MNL")), ("airasia", ("PEK", "KUL"))],
            3600
        )

        schedule2 = generate_schedule(
            date(2016, 5, 1),
            date(2016, 5, 8),
            [("airasia", ("KUL", "MEL")), ("airasia", ("KUL", "CMB")), ("airasia", ("PEK", "CMB")), ("airasia", ("PEK", "MEL"))],
            3600,
            days_offset=0,
        )

        for item in schedule2:
            job = {
                "flight_date": item[0],
                "airline": item[1],
                "origin": item[2],
                "destination": item[3],
                "period": item[4],
                "next_run_after": date(2016, 1, 1),
            }
            job_id = CrawlJob.upsert(**job)
            print CrawlJob.get(job_id)


if __name__ == '__main__':
    main()
