from financial_data.config.env import run_migrations
from financial_data.iex.models import IexBase

run_migrations(IexBase.metadata, IexBase.metadata.schema)
