from sqlalchemy import MetaData

from financial_data.core.base import ModelBase

SCHEMA = "iex"


class IexBase(ModelBase):
    __abstract__ = True
    metadata = MetaData(schema=SCHEMA)
