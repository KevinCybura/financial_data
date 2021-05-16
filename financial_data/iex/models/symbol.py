import enum
from datetime import date
from typing import Optional

from pydantic import Field
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

from financial_data.core import BaseModel
from financial_data.core.utils import to_camel
from financial_data.iex.models.meta import IexBase


class SymbolTypes(str, enum.Enum):
    ad = "ad"
    cs = "cs"
    cef = "cef"
    et = "et"
    oef = "oef"
    ps = "ps"
    rt = "rt"
    struct = "struct"
    ut = "ut"
    wi = "wi"
    wt = "wt"
    crypto = "crypto"


class Symbol(IexBase):
    symbol = Column(String, unique=True)
    exchange_id = Column(String, ForeignKey("exchange.exchange"), nullable=True)
    exchange: "Exchange" = relationship("Exchange", backref=backref("symbols"))  # type: ignore
    name = Column(String)
    date = Column(Date)
    is_enabled = Column(Boolean)
    region = Column(String)
    currency = Column(String)
    iex_id = Column(String)
    figi = Column(String, nullable=True)
    cik = Column(String, nullable=True)

    type = Column(Enum(SymbolTypes, name="symbol_type"), nullable=True)

    def __repr__(self) -> str:
        return f"<Symbol(symbol={self.symbol}, name={self.name}, id={self.id})>"


class IexSymbol(BaseModel):
    symbol: str
    exchange_id: Optional[str] = Field(alias="exchange")
    name: str
    date: date
    is_enabled: bool
    region: str
    currency: str
    iex_id: Optional[str]
    figi: Optional[str]
    cik: Optional[str]
    type: Optional[SymbolTypes]

    class Config:
        alias_generator = to_camel
        model = Symbol
        allow_population_by_field_name = True
