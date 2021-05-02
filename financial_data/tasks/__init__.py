import functools
from typing import Callable
from typing import Iterable

from prefect import Task as PrefectTask

from financial_data.types import RunType


class SkipRecordException(Exception):
    pass


class Task(PrefectTask):
    def __init__(self, run_type: RunType = "dataset", dataset: str = "dataset", **kwargs):
        super().__init__(**kwargs)
        self.run_type = run_type
        self.dataset = dataset
        if run_type == "record":
            record_run = self.run
            self.run = functools.partial(self._run, func=record_run)

    def _run(self, func: Callable, dataset: Iterable, **kwargs) -> Iterable:
        def _map(data):
            try:
                return func(data, **kwargs)
            except SkipRecordException as e:
                return e

        def _filter(data):
            if isinstance(data, SkipRecordException):
                return False
            return True

        return list(filter(_filter, map(_map, dataset)))
