import prefect
import requests
from prefect import Flow
from prefect import Task
from prefect import task
from prefect.executors import LocalDaskExecutor
from prefect.run_configs import LocalRun
from prefect.storage import Local

from financial_data.tasks import IexSettings
from financial_data.tasks import IexTask


@task(tags=["iex-core-data"])
class ExtractSymbols(IexTask):
    def run(self):
        settings = prefect.context.settings
        symbols = requests.get(settings.url + "/ref-data/symbols", params={"token": settings.token.get_secret_value()})

        if symbols.status_code != 200:
            prefect.context.get("logger").error(f"Failed to get symbols, err={symbols.text}")

        return symbols.json()


extract_symbols = ExtractSymbols()


@task(tags=["iex-core-data"])
def extract_exchanges():
    settings = prefect.context.settings
    exchanges = requests.get(settings.url + "/ref-data/exchanges", params={"token": settings.token.get_secret_value()})

    if exchanges.status_code != 200:
        prefect.context.get("logger").error(f"Failed to get exchanges, err={exchanges.text}")

    return exchanges.json()


@task(tags=["iex-core-data"])
def extract_us_exchanges():
    settings = prefect.context.settings
    exchanges = requests.get(
        settings.url + "/ref-data/market/us/exchanges", params={"token": settings.token.get_secret_value()}
    )

    if exchanges.status_code != 200:
        prefect.context.get("logger").error(f"Failed to get us exchanges, err={exchanges.text}")

    return exchanges.json()


with Flow("iex-core-data", storage=Local(stored_as_script=True, path="flows/core_data.py")) as flow:

    extract_symbols()
    extract_exchanges()
    extract_us_exchanges()


flow.run_config = LocalRun(labels=["iex-core-data", "kevincybura-X570-UD"])
flow.executor = LocalDaskExecutor()

with prefect.context(settings=IexSettings()):
    flow.run()
