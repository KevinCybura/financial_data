from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.sql.sqltypes import String

from financial_data.base import ModelBase


class UsExchange(ModelBase):
    __tablename__ = "us_exchange"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    long_name = Column(String)
    mic = Column(String)
    tape_id = Column(String)
    oats_id = Column(String)
    ref_id = Column(String)
    type = Column(String)

    def __repr__(self) -> str:
        return f"<UsExchange(name={self.name}, long_name={self.long_name}, id={self.id})>"
