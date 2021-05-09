from types import TracebackType
from typing import Any
from typing import MutableMapping
from typing import Optional
from typing import Type
from typing import Union

from sqlalchemy import Column

from financial_data.core.base import BaseModel
from financial_data.core.base import ModelBase

OptionalStr = Optional[str]

# SQL alchemy types.
Col = Union[Column, str]
Table = ModelBase

# __exit__ types
SomeException = Optional[BaseException]
SomeExceptionType = Optional[Type[BaseException]]
SomeTracebackType = Optional[TracebackType]

# Task types.
Record = Union[MutableMapping[str, Any], Table, BaseModel, "Skip"]


class Skip:
    def __init__(self, record: Record):
        self.record = record
