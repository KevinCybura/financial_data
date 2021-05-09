import os
from enum import Enum

from financial_data.core.database import DataBase
from financial_data.core.database import PostgresSettings
from financial_data.iex import IexSettings

IEX_SETTINGS = IexSettings()

POSTGRES_SETTINGS = PostgresSettings()
DATABASE = DataBase(
    database=POSTGRES_SETTINGS.database.get_secret_value(),
    user=POSTGRES_SETTINGS.user.get_secret_value(),
    password=POSTGRES_SETTINGS.password.get_secret_value(),
    host=POSTGRES_SETTINGS.host.get_secret_value(),
    port=POSTGRES_SETTINGS.port.get_secret_value(),
)


class EnvType(Enum):
    LOCAL = "local"
    PROD = "prod"


# TODO: figure out how to set AGENT_ENVIRONMENT using prefect secrets here.
ENVIRONMENT = EnvType(os.environ.get("AGENT_ENVIRONMENT", "local"))
