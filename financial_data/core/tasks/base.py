from typing import Any
from typing import Callable
from typing import Iterable
from typing import Optional
from typing import Sequence

from prefect import Task as PrefectTask

from financial_data.core.types import Record
from financial_data.core.types import Skip


class BaseTask(PrefectTask):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.kw = kwargs

    def filter_map_records(self, dataset: Iterable[Record], **kwargs: Any) -> "PrefectTask":
        return FilterMapTask(**self.kw)(dataset, self.run, **kwargs)

    def map_records(self, dataset: Iterable[Record], **kwargs: Any) -> "PrefectTask":
        return MapTask(**self.kw)(dataset, self.run, **kwargs)

    def filter_records(self, dataset: Iterable[Record], **kwargs: Any) -> "PrefectTask":
        return FilterTask(**self.kw)(dataset, self.run, **kwargs)


class MapTask(BaseTask):
    def run(self, dataset: Iterable[Record], run: Callable[..., Record], **kwargs: Any) -> Optional[Sequence[Record]]:  # type: ignore[override]
        """ If the run method is defined to take one element apply the run function to each record. """
        return [run(data) for data in dataset]


class FilterTask(BaseTask):
    def run(self, dataset: Iterable[Record], run: Callable[..., bool], **kwargs: Any) -> Optional[Sequence[Record]]:  # type: ignore[override]
        """
        If the run method is defined to take one element and returns a bool apply the run function to each record
        and skip if True or False is returned.
        """
        filtered_dataset = []
        for data in dataset:
            if run(data):
                filtered_dataset.append(data)

        return filtered_dataset


class FilterMapTask(BaseTask):
    def run(self, dataset: Iterable[Record], run: Callable[..., Record], **kwargs: Any) -> Optional[Sequence[Record]]:  # type: ignore[override]
        """
        If the run method is defined to take one element apply the run function to each record. The record is
        skipped if a Skip object is returned.
        """
        mapped_dataset = []
        for record in dataset:
            mapped_record = run(record, **kwargs)
            if isinstance(mapped_record, Skip):
                continue
            mapped_dataset.append(mapped_record)

        return mapped_dataset
