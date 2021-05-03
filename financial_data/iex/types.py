from typing import Union

from .models.exchange import IexExchange
from .models.symbol import IexSymbol

IexModel = Union[IexSymbol, IexExchange]
