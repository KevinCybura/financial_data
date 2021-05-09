from typing import Any
from typing import List
from typing import Sequence
from typing import Type

from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import Select

from financial_data.core.database import DataBase
from financial_data.core.types import Col
from financial_data.core.types import Table

from .base import BaseTask

# mypy: ignore-errors


class SelectTask(BaseTask):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.database = DataBase()

    def run(self) -> Sequence[Table]:
        with self.database as session:
            return session.execute(self.stmt()).scalars().all()

    def stmt(self) -> Select:
        raise NotImplementedError


class UpsertTask(BaseTask):
    def __init__(self, model: Type[Table], index_columns: List[Col] = None, **kwargs: Any):
        self.database = DataBase()
        self.table_name = model.__table__
        self.model = model
        if index_columns is None:
            index_columns = [model.id]
        self.index_columns = index_columns
        super().__init__(**kwargs)

    def run(self, data: List[dict]) -> None:
        stmt = postgresql.insert(self.table_name).values(data)
        update_stmt = stmt.on_conflict_do_update(index_elements=self.index_columns, set_=stmt.excluded)
        self.database.engine.execute(update_stmt)
