from typing import Optional

from pydantic import Field
from pydantic import PostgresDsn
from pydantic import SecretStr
from pydantic import validator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from .base import BaseSettings
from .types import SomeException
from .types import SomeExceptionType
from .types import SomeTracebackType


class PostgresSettings(BaseSettings):
    drivername: str = Field("postgresql")
    user: SecretStr = Field("fin_data")
    password: SecretStr = Field("fin_data")
    host: SecretStr = Field("localhost")
    port: SecretStr = Field(5432)
    database: SecretStr = Field("fin_data")
    url: PostgresDsn = None  # type: ignore

    class Config(BaseSettings.Config):
        env_prefix = "postgres_"
        case_sensitive = False

    @validator("url")
    def postgres_uri(cls, _v: PostgresDsn, values: dict) -> PostgresDsn:
        return PostgresDsn.build(  # type: ignore
            scheme="postgresql",
            user=values["user"].get_secret_value(),
            password=values["password"].get_secret_value(),
            host=values["host"].get_secret_value(),
            port=values["port"].get_secret_value(),
            path=f"/{values['database'].get_secret_value()}",
        )


class DataBase:
    def __init__(
        self,
        *,
        database: str = None,
        user: str = None,
        password: str = None,
        host: str = None,
        port: str = None,
        settings: PostgresSettings = None,
    ):
        self.settings = settings
        if not all([database, user, password, host, port]):
            self.settings = PostgresSettings()
        else:
            self.settings = PostgresSettings(database=database, user=user, password=password, host=host, port=port)

        self.engine = create_engine(self.settings.url)

        self.session_cls = sessionmaker(self.engine)

    def __enter__(self) -> Session:
        self._session = self.session_cls()
        return self._session

    def __exit__(self, _: SomeExceptionType, _exc: SomeException, _tb: SomeTracebackType) -> Optional[bool]:
        self._session.close()
        return None
