import enum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

from financial_data.base import Base

if TYPE_CHECKING:
    from financial_data.models import Exchange


class SymbolTypes(enum.Enum):
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
    empty = None


class Symbol(Base):
    __tablename__ = "symbol"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True)
    exchange_id = Column(String, ForeignKey("exchange.exchange"))
    exchange: "Exchange" = relationship("Exchange", backref=backref("symbols"))
    name = Column(String)
    date = Column(Date)
    is_enabled = Column(Boolean)
    region = Column(String)
    currency = Column(String)
    iex_id = Column(String)
    figi = Column(String, nullable=True)
    cik = Column(String, nullable=True)

    type = Column(Enum(SymbolTypes, name="symbol_type"), nullable=True)

    def __repr__(self):
        return f"<Symbol(symbol={self.symbol}, name={self.name}, id={self.id})>"
