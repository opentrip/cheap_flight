# coding: utf-8
# ./manage.py script cheapflight.scripts.rader:main

from datetime import datetime, timedelta
from cheapflight.models.rader import fetch_lowest_price
from cheapflight.models.crawl_job import CrawlJob


def main():
    now = datetime.now()
    all_jobs = CrawlJob.get_jobs(now)
    # print len(all_jobs)
    for crawl_job in all_jobs:
        try:
            price = fetch_lowest_price(
                crawl_job.airline,
                crawl_job.origin,
                crawl_job.destination,
                crawl_job.flight_date,
                crawl_job.period,
            )
            if price is None:
                print "%s: ERROR" % (crawl_job,)
            else:
                # TODO 处理无可用航班与查询出错的情况
                print "%s: Y%d" % (crawl_job, price)
            next_run_after = now + \
                timedelta(seconds=crawl_job.period)
            crawl_job.update(
                next_run_after=next_run_after
            )
        except:
            pass


if __name__ == '__main__':
    main()
