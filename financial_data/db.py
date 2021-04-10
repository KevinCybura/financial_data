from typing import Any
from typing import Union

from pydantic import Field
from pydantic import SecretStr
from pydantic import validator
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from financial_data.base import Base
from financial_data.base import BaseModel
from financial_data.base import BaseSettings


class PostgresSettings(BaseSettings):
    drivername: str = "postgresql"
    username: SecretStr = Field("fin_data", env="username")
    password: SecretStr = Field("fin_data", env="password")
    host: SecretStr = Field("localhost", env="host")
    port: SecretStr = Field(5432, env="port")
    database: SecretStr = Field("fin_data", env="database")
    url: Union[URL, str] = ""

    class Config:
        env_prefix = "postgres"
        case_sensitive = False

    @validator("url", always=True)
    def create_url(cls, v: Union[URL, str], values: dict, **kwargs: dict) -> Union[URL, str]:
        if v:
            return v

        secret_values: dict[str, Any] = {}
        for k, v in values.items():
            if isinstance(v, SecretStr):
                secret_values[k] = v.get_secret_value()
            else:
                secret_values[k] = v

        return URL.create(**secret_values)


class DataBase(BaseModel):
    engine: Engine
    session: Session
    _settings: PostgresSettings

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self, database: str = None, user: str = None, password: str = None, host: str = None, port: str = None
    ):

        credentials = PostgresSettings(database=database, user=user, password=password, host=host, port=port)

        engine = create_engine(credentials.url)

        session = sessionmaker(engine)

        Base.metadata.create_all(engine)

        super().__init__(
            engine=engine,
            session=session,
            _credentials=credentials,
        )
