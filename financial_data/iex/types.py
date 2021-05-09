from typing import Union

from .models import IexExchange
from .models import IexSymbol

IexModel = Union[IexSymbol, IexExchange]
