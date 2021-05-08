from typing import Any
from typing import Callable
from typing import Iterable
from typing import Optional
from typing import Sequence

from prefect import Task as PrefectTask


class SkipRecordException(Exception):
    """Used to skip records in MapTask."""

    pass


class MapTask(PrefectTask):
    def run(self, dataset: Iterable, run: Callable, **kwargs: Any) -> Optional[Sequence]:  # type: ignore[override]
        """
        If the run method is defined to take one element this function then map_records will call run for each item.
        """
        transformed_records = []
        for record in dataset:
            try:
                transformed_records.append(run(record, **kwargs))
            except SkipRecordException:
                pass

        return transformed_records


class Task(PrefectTask):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.task_kwargs = kwargs

    def map_records(self, dataset: Iterable, **kwargs: Any) -> PrefectTask:
        return MapTask(**self.task_kwargs)(dataset, self.run, **kwargs)
