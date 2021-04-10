from sqlalchemy import Column
from sqlalchemy import String

from financial_data.base import Base


class Exchange(Base):
    __tablename__ = "exchange"

    exchange = Column(String, primary_key=True)
    region = Column(String)
    description = Column(String)
    mic = Column(String)
    exchange_suffix = Column(String)

    def __repr__(self):
        return f"<Exchange(exchange={self.exchange}, exchange_suffix={self.exchange_suffix})>"
