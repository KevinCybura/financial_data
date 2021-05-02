from pydantic import Field
from pydantic import HttpUrl
from pydantic import SecretStr

from financial_data.base import BaseSettings


class IexSettings(BaseSettings):
    token: SecretStr
    url: HttpUrl = Field("https://sandbox.iexapis.com")
    _sandbox: bool = None

    class Config(BaseSettings.Config):
        env_prefix = "iex_"
        case_sensitive = False
        prefect_secrets = False
