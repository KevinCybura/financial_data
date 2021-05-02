from typing import Literal
from typing import Optional
from typing import Union

from sqlalchemy import Column
from sqlalchemy.orm.decl_api import DeclarativeMeta

OptionalStr = Optional[str]
# Task types
RunType = Literal["record", "dataset"]

# SQL alchemy types.
Col = Union[Column, str]
Table = DeclarativeMeta
