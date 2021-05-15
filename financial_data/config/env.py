from collections import Callable
from logging.config import fileConfig
from typing import Optional

from alembic import context
from sqlalchemy import MetaData
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from financial_data.config.common import POSTGRES_SETTINGS

config = context.config


fileConfig(config.config_file_name)


def _include_object(target_schema: Optional[str]) -> Callable:
    def include_object(obj: MetaData, name: str, object_type: str, reflected: str, compare_to: str) -> bool:
        if object_type == "table":
            return obj.schema == target_schema
        else:
            return True

    return include_object


def _run_migrations_offline(target_metadata: MetaData, schema: Optional[str]) -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = POSTGRES_SETTINGS.url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        include_schemas=True,
        include_object=_include_object(schema),
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def _run_migrations_online(target_metadata: MetaData, schema: Optional[str]) -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=POSTGRES_SETTINGS.url,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,  # 2
            include_object=_include_object(schema),  # 2
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations(metadata: MetaData, schema: Optional[str]) -> None:
    if context.is_offline_mode():
        _run_migrations_offline(metadata, schema)
    else:
        _run_migrations_online(metadata, schema)
