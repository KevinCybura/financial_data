from typing import List

import requests
from prefect import Task

from financial_data.iex import IexSettings


class IexApiTask(Task):
    def __init__(self, endpoint, **kwargs):
        self.secrets = IexSettings()
        self.endpoint = endpoint
        self.url = self.secrets.url + endpoint
        self.params = {"token": self.secrets.token.get_secret_value()}
        super().__init__(**kwargs)

    def run(self) -> List[dict]:  # type: ignore
        response = requests.get(self.url, params=self.params)

        if response.status_code != 200:
            self.logger.error(
                f"Failed to extract data from iex endpoint={self.endpoint}",
                extra={"url": self.url, "error": response.text, "status": response.status_code},
            )
            raise requests.HTTPError()

        self.logger.info(f"Data extracted from endpoint={self.endpoint}")

        return response.json()
