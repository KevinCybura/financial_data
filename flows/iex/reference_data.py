from prefect import Flow

from financial_data.core.tasks import UpsertTask
from financial_data.iex import IexApiTask
from financial_data.iex.models import Exchange
from financial_data.iex.models import IexExchange
from financial_data.iex.models import IexSymbol
from financial_data.iex.models import Symbol
from financial_data.iex.tasks.reference_data import SelectExchanges
from financial_data.iex.tasks.reference_data import SymbolsTransformRefData
from financial_data.iex.tasks.reference_data import TransformRefData
from flows.iex.run_config import reference_data_config

extract_symbols = IexApiTask(name="extract-symbols", endpoint="/ref-data/symbols")

extract_exchanges = IexApiTask(name="extract-exchanges", endpoint="/ref-data/exchanges")

extract_us_exchanges = IexApiTask(endpoint="/ref-data/market/us/exchanges")

select_exchanges = SelectExchanges(name="select-exchanges")


transform_ref_data = TransformRefData(name="transform-ref-data")

symbol_transform_ref_data = SymbolsTransformRefData(name="symbol-transform-ref-data")


load_symbols = UpsertTask(model=Symbol, index_columns=[Symbol.symbol], name="load-symbols")
load_exchanges = UpsertTask(model=Exchange, index_columns=[Exchange.exchange], name="load-exchanges")

with Flow("iex-ref-data") as flow:
    exchanges = transform_ref_data.filter_map_records(dataset=extract_exchanges(), model=IexExchange)

    load_exchanges(exchanges)
    symbols = symbol_transform_ref_data.filter_map_records(
        dataset=extract_symbols(), exchanges=select_exchanges(), model=IexSymbol
    )
    load_symbols(symbols)


flow.run_config = reference_data_config(["iex-data"])

if __name__ == "__main__":
    flow.run()
