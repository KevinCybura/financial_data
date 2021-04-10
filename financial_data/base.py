from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Tuple

from prefect.tasks.secrets import PrefectSecret
from pydantic import BaseModel as PydanticBaseModel
from pydantic import BaseSettings as PydanticBaseSettings
from pydantic.env_settings import SettingsSourceCallable
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(PydanticBaseModel):
    pass


class BaseSettings(PydanticBaseSettings):
    class Config:
        prefect_secrets = False

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            if cls.prefect_secrets:
                prefect_settings: SettingsSourceCallable = PrefectSettings()
                return prefect_settings, init_settings, env_settings, file_secret_settings
            return init_settings, env_settings, file_secret_settings


class PrefectSettings:
    """
    A pydantic callable that is used to get environment variables from prefect for the pydantic BaseSettings class
    """

    def __call__(self, settings: PydanticBaseSettings) -> Dict[str, Any]:
        d: Dict[str, Optional[str]] = {}

        for field in settings.__fields__.values():
            env_val: Optional[str] = None
            for env_name in field.field_info.extra["env_names"]:
                env_val = PrefectSecret(env_name).run()

            d[field.alias] = env_val

        return d
