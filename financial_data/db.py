from pydantic import Field
from pydantic import PostgresDsn
from pydantic import SecretStr
from pydantic import validator
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from financial_data.base import Base
from financial_data.base import BaseModel
from financial_data.base import BaseSettings


class PostgresSettings(BaseSettings):
    drivername: str = Field("postgresql")
    user: SecretStr = Field("fin_data")
    password: SecretStr = Field("fin_data")
    host: SecretStr = Field("localhost")
    port: SecretStr = Field(5432)
    database: SecretStr = Field("fin_data")
    url: PostgresDsn = Field(None)

    class Config:
        env_prefix = "postgres_"
        case_sensitive = False

    @validator("url")
    def postgres_uri(cls, _v: PostgresDsn, values: dict) -> str:
        return PostgresDsn.build(
            scheme="postgresql",
            user=values["user"].get_secret_value(),
            password=values["password"].get_secret_value(),
            host=values["host"].get_secret_value(),
            port=values["port"].get_secret_value(),
            path=f"/{values['database'].get_secret_value()}",
        )


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