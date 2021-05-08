from typing import Any
from typing import Set
from typing import Type

from sqlalchemy import select

from financial_data.db import DataBase
from financial_data.iex import IexModel
from financial_data.iex.models import Exchange
from financial_data.iex.models import IexSymbol
from financial_data.tasks import SkipRecordException
from financial_data.tasks import Task


class TransformRefData(Task):
    def run(self, data: dict, model: Type[IexModel]) -> dict:  # type: ignore[override]
        return model(**data).dict()


class SymbolsTransformRefData(Task):
    def run(self, data: dict, exchanges: Set[Exchange], model: Type[IexSymbol]) -> dict:  # type: ignore[override]
        validated_data = model(**data)
        if validated_data.exchange_id not in exchanges:
            raise SkipRecordException
        return validated_data.dict()


class SelectExchanges(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.database = DataBase()

    def run(self) -> Set[str]:  # type: ignore[override]
        with self.database.session as session:
            return set(session.execute(select(Exchange.exchange)).scalars())
