from sqlalchemy import Column
from sqlalchemy import String

from financial_data.core import BaseModel
from financial_data.core.utils import to_camel
from financial_data.iex.models.meta import IexBase


class Exchange(IexBase):
    exchange = Column(String, unique=True)
    region = Column(String)
    description = Column(String)
    mic = Column(String)
    exchange_suffix = Column(String)

    def __repr__(self) -> str:
        return f"<Exchange(exchange={self.exchange}, exchange_suffix={self.exchange_suffix})>"


class IexExchange(BaseModel):
    exchange: str
    region: str
    description: str
    mic: str
    exchange_suffix: str

    class Config:
        alias_generator = to_camel
