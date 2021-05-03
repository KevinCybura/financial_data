from typing import Type

from prefect import Flow
from prefect.run_configs import LocalRun

from financial_data.iex import IexApiTask
from financial_data.iex import IexModel
from financial_data.iex.models import Exchange
from financial_data.iex.models import IexExchange
from financial_data.iex.models import IexSymbol
from financial_data.iex.models import Symbol
from financial_data.tasks import Task
from financial_data.tasks.database import UpsertTask

extract_symbols = IexApiTask(name="extract-symbols", endpoint="/ref-data/symbols", slug="extract-symbols")

extract_exchanges = IexApiTask(name="extract-exchanges", endpoint="/ref-data/exchanges", slug="extract-exchanges")

extract_us_exchanges = IexApiTask(endpoint="/ref-data/market/us/exchanges")


class TransformRefData(Task):
    def run(self, data: dict, model: Type[IexModel]) -> Dict[str, Any]:  # type: ignore
        return model(**data).dict()


class SymbolsTransformRefData(Task):
    def run(self, data: dict, model: Type[IexSymbol]) -> dict:  # type: ignore
        # TODO Make sure exchanges in DB.
        del data["exchange"]
        return model(**data).dict()


transform_ref_data = TransformRefData(name="transform-ref-data", slug="transform-reference-data", run_type="record")
symbol_transform_ref_data = SymbolsTransformRefData(
    name="symbol-transform-ref-data", slug="symbol-transform-reference-data", run_type="record"
)


load_symbols = UpsertTask(model=Symbol, conflict_columns=[Symbol.symbol], slug="load-symbols", name="load-symbols")
load_exchanges = UpsertTask(
    model=Exchange, conflict_columns=[Exchange.exchange], slug="load-exchanges", name="load-exchanges"
)

with Flow("iex-ref-data") as flow:
    load_symbols(symbol_transform_ref_data(dataset=extract_symbols(), model=IexSymbol))
    load_exchanges(transform_ref_data(dataset=extract_exchanges(), model=IexExchange))


flow.run_config = LocalRun(labels=["iex-ref-data"])

if __name__ == "__main__":
    flow.run()
