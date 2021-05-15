from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Type

from prefect.tasks.secrets import PrefectSecret
from pydantic import BaseModel as PydanticBaseModel
from pydantic import BaseSettings as PydanticBaseSettings
from pydantic.env_settings import SettingsSourceCallable
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import deferred
from sqlalchemy.orm.decl_api import as_declarative
from sqlalchemy.orm.decl_api import declared_attr


@as_declarative()
class ModelBase:
    @declared_attr
    def __tablename__(self) -> Mapped[str]:
        return self.__name__.lower()

    @declared_attr
    def id(self) -> Mapped[Integer]:
        return Column(Integer, autoincrement=True, primary_key=True)

    @declared_attr
    def created_at(self) -> Mapped[DateTime]:
        return deferred(Column(DateTime, default=func.now()))

    @declared_attr
    def updated_at(self) -> Mapped[DateTime]:
        return deferred(Column(DateTime, onupdate=func.now()))


class BaseSettings(PydanticBaseSettings):
    class Config:
        prefect_secrets = False
        env_file = ".env"
        allow_population_by_field_name = True

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:

            if cls.prefect_secrets:
                return init_settings, env_settings, file_secret_settings, PrefectSettings()
            return init_settings, env_settings, file_secret_settings


class BaseModel(PydanticBaseModel):
    class Config:
        model: Optional[Type[Table]] = None

    def to_model(self) -> Table:
        return self.Config.model(**self.dict())  # type: ignore


class PrefectSettings:
    """
    A pydantic callable that is used to get environment variables from prefect for the pydantic BaseSettings class
    """

    def __call__(self, settings: PydanticBaseSettings) -> Dict[str, Any]:
        d: Dict[str, Optional[str]] = {}
        for field in settings.__fields__.values():
            for env_name in field.field_info.extra["env_names"]:
                try:
                    env_val = PrefectSecret(env_name).run()  # type: ignore
                    d[field.alias] = env_val
                    break
                except ValueError:
                    pass

        return d
