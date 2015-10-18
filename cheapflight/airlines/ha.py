# coding: utf-8
import functools


class HighAvailabilitySearcher(object):
    def __init__(self, searcher_list):
        if not isinstance(searcher_list, list):
            searcher_list = list(searcher_list)
        self.searcher_list = searcher_list
        self.failed_counter = [0] * len(self.searcher_list)
        self.i = 0

    def _get_searcher(self):
        if len(self.searcher_list) == 1 or self.failed_counter[self.i] == 0:
            return self.searcher_list[self.i]

        self.i = min(
            xrange(len(self.searcher_list)),
            key=lambda i: self.failed_counter[i]
        )

        return self.searcher_list[self.i]

    def __getattr__(self, name):
        searcher = self._get_searcher()

        raw_attr = getattr(searcher, name)
        if not callable(raw_attr):
            return raw_attr

        raw_fn = raw_attr

        @functools.wraps(raw_fn)
        def _(*args, **kwargs):

            try:
                return raw_fn(*args, **kwargs)
            except:
                self.failed_counter[self.i] += 2
                raise
            else:
                if self.failed_counter[self.i] > 0:
                    self.failed_counter[self.i] -= 1
        return _
