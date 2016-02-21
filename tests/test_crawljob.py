# coding: utf-8
from datetime import date, datetime

from base_test_case import BaseTestCase
from cheapflight.models.crawl_job import CrawlJob


class CrawJobTestCase(BaseTestCase):

    def test_list_jobs(self):
        job_id = CrawlJob.add(
            flight_date=date(2016, 10, 10),
            airline="airasia",
            origin="PEK",
            destination="KUL",
            next_run_after=date(2000, 1, 1),
        )

        job_id2 = CrawlJob.add(
            flight_date=date(2016, 10, 11),
            airline="airasia",
            origin="PEK",
            destination="KUL",
            next_run_after=date(2001, 1, 1),
        )
        assert len(CrawlJob.get_jobs(at=datetime(2016, 1, 1))) == 2
        assert len(CrawlJob.get_jobs(at=datetime(2000, 2, 2))) == 1
        assert len(CrawlJob.get_jobs(at=datetime(1999, 2, 2))) == 0
        CrawlJob.delete(job_id)
        CrawlJob.delete(job_id2)
