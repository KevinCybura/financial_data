from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

SCHEMA = "iex"

metadata = MetaData(schema=SCHEMA)

IexBase = declarative_base(name="IexBase", metadata=metadata)
