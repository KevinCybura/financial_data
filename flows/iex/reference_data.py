from prefect import Flow
from prefect import unmapped

from financial_data.core.tasks import UpsertTask
from financial_data.iex.models import Exchange
from financial_data.iex.models import IexExchange
from financial_data.iex.models import IexSymbol
from financial_data.iex.models import Symbol
from financial_data.iex.tasks import IexApiTask
from financial_data.iex.tasks.reference_data import SymbolsTransformRefData
from financial_data.iex.tasks.reference_data import TransformRefData
from flows.iex.run_config import reference_data_config

extract_symbols = IexApiTask(name="extract-symbols")

extract_exchanges = IexApiTask(name="extract-exchanges")


transform_ref_data = TransformRefData(name="transform-ref-data")

symbol_transform_ref_data = SymbolsTransformRefData(name="symbol-transform-ref-data")


load_symbols = UpsertTask(model=Symbol, index_columns=[Symbol.symbol], name="load-symbols")
load_exchanges = UpsertTask(
    model=Exchange, index_columns=[Exchange.exchange], returning=[Exchange.exchange], name="load-exchanges"
)

with Flow("iex-ref-data") as flow:
    exchanges = transform_ref_data.filter_map_records(
        dataset=extract_exchanges(endpoint="/ref-data/exchanges"), model=IexExchange
    )

    stored_exchanges = load_exchanges(exchanges)

    symbols = extract_symbols.map(
        endpoint=[
            "/ref-data/symbols",
            "/ref-data/crypto/symbols",
            "/ref-data/mutual-funds/symbols",
            "/ref-data/otc/symbols",
        ]
    )
    transformed_symbols = symbol_transform_ref_data.filter_map_datasets(
        datasets=symbols, exchanges=unmapped(stored_exchanges), model=unmapped(IexSymbol)
    )
    load_symbols.map(transformed_symbols)


flow.run_config = reference_data_config(["iex-data"])

if __name__ == "__main__":
    flow.run()
