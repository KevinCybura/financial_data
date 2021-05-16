from typing import Any
from typing import Optional

import requests

from financial_data.config.common import IEX_SETTINGS
from financial_data.core.tasks.base import BaseTask


class IexApiTask(BaseTask):
    def __init__(self, **kwargs: Any):
        self.secrets = IEX_SETTINGS
        self.params = {"token": self.secrets.token.get_secret_value()}
        super().__init__(**kwargs)

    def run(self, endpoint: str) -> Any:  # type: ignore[override]
        url = self.secrets.url + endpoint

        response = requests.get(url, params=self.params)

        if response.status_code != 200:
            self.logger.error(
                f"Failed to extract data from iex endpoint={endpoint}",
                extra={"url": url, "error": response.text, "status": response.status_code},
            )
            raise requests.HTTPError()

        self.logger.info(f"Data extracted from endpoint={endpoint}")

        return response.json()
