from typing import Literal
from typing import Optional
from typing import Union

from sqlalchemy import Column

from financial_data.base import ModelBase

OptionalStr = Optional[str]

# SQL alchemy types.
Col = Union[Column, str]
Table = ModelBase
