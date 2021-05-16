from typing import Any
from typing import List
from typing import Set
from typing import Type

from sqlalchemy import select

from financial_data.config.common import DATABASE
from financial_data.core.tasks import BaseTask
from financial_data.core.types import Record
from financial_data.core.types import Skip
from financial_data.iex import IexModel
from financial_data.iex.models import Exchange
from financial_data.iex.models import IexSymbol


class TransformRefData(BaseTask):
    def run(self, data: dict, model: Type[IexModel]) -> Record:  # type: ignore[override]
        return model(**data).dict()


class SymbolsTransformRefData(BaseTask):
    def run(self, data: dict, exchanges: List[Exchange], model: Type[IexSymbol]) -> Record:  # type: ignore[override]
        unique_exchanges = set(exchanges)
        validated_data = model(**data)
        if validated_data.exchange_id and validated_data.exchange_id not in unique_exchanges:
            return Skip(validated_data.dict())

        return validated_data.dict()


class SelectExchanges(BaseTask):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def run(self) -> Set[str]:  # type: ignore[override]
        with DATABASE as session:
            return set(session.execute(select(Exchange.exchange)).scalars())
