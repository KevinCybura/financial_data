import functools
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Union

from prefect import Task as PrefectTask

from financial_data.types import RunType


class SkipRecordException(Exception):
    pass


class Task(PrefectTask):
    def __init__(self, run_type: RunType = "dataset", dataset: str = "dataset", **kwargs: Any):
        super().__init__(**kwargs)
        self.run_type = run_type
        self.dataset = dataset
        if run_type == "record":
            record_run = self.run
            self.run = functools.partial(self._run, run=record_run)  # type: ignore

    def _run(self, run: Callable, dataset: Iterable, **kwargs: Any) -> Iterable:
        def _map(data: Any) -> Union[Any, SkipRecordException]:
            try:
                return run(data, **kwargs)
            except SkipRecordException as e:
                return e

        def _filter(data: Any) -> bool:
            if isinstance(data, SkipRecordException):
                return False
            return True

        return list(filter(_filter, map(_map, dataset)))
