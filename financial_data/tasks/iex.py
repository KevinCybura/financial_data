from datetime import date
from typing import Optional

from prefect import Task
from pydantic import Field
from pydantic import HttpUrl
from pydantic import SecretStr
from pydantic.utils import to_camel

from financial_data.base import BaseModel
from financial_data.base import BaseSettings
from financial_data.models.symbol import SymbolTypes


class IexSettings(BaseSettings):
    token: SecretStr
    url: HttpUrl = Field("https://sandbox.iexapis.com")
    _sandbox: Optional[bool] = None

    class Config:
        env_prefix = "iex_"
        case_sensitive = False
        prefect_secrets = False


class Symbol(BaseModel):
    symbol: str
    exchange: str
    name: str
    date: date
    is_enabled: bool
    region: str
    currency: str
    iex_id: str
    figi: Optional[str]
    cik: Optional[str]
    type: SymbolTypes

    class Config:
        alias_generator = to_camel


class IexTask(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secrets = IexSettings()
