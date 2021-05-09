from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Type

from prefect.tasks.secrets import PrefectSecret
from pydantic import BaseModel as PydanticBaseModel
from pydantic import BaseSettings as PydanticBaseSettings
from pydantic.env_settings import SettingsSourceCallable
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base

ModelBase = declarative_base(name="ModelBase")


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
        model: Type[Table] = None  # type: ignore

    def to_model(self) -> Table:
        return self.Config.model(**self.dict())


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
