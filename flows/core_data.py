import prefect
import requests
from prefect import Flow
from prefect.run_configs import LocalRun

from financial_data.tasks import IexTask


class ExtractSymbols(IexTask):
    def run(self):
        symbols = requests.get(
            self.secrets.url + "/ref-data/symbols", params={"token": self.secrets.token.get_secret_value()}
        )

        if symbols.status_code != 200:
            prefect.context.get("logger").error(f"Failed to get symbols, err={symbols.text}")

        return symbols.json()


extract_symbols = ExtractSymbols()


class ExtractExchanges(IexTask):
    def run(self):
        exchanges = requests.get(
            self.secrets.url + "/ref-data/exchanges", params={"token": self.secrets.token.get_secret_value()}
        )

        if exchanges.status_code != 200:
            prefect.context.get("logger").error(f"Failed to get exchanges, err={exchanges.text}")

        return exchanges.json()


extract_exchanges = ExtractExchanges()


class ExtractUsExchanges(IexTask):
    def run(self):
        exchanges = requests.get(
            self.secrets.url + "/ref-data/market/us/exchanges",
            params={"token": self.secrets.token.get_secret_value()},
        )

        if exchanges.status_code != 200:
            prefect.context.get("logger").error(f"Failed to get us exchanges, err={exchanges.text}")

        return exchanges.json()


extract_us_exchanges = ExtractUsExchanges()

with Flow("iex-core-data") as flow:
    extract_symbols()
    extract_exchanges()
    extract_us_exchanges()


flow.run_config = LocalRun(labels=["kevincybura-X570-UD"])

if __name__ == "__main__":
    flow.run()
