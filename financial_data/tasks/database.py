from typing import Any
from typing import List
from typing import Sequence
from typing import Type

from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import Select

from financial_data.db import DataBase
from financial_data.tasks import Task
from financial_data.types import Col
from financial_data.types import Table

# mypy: ignore-errors


class SelectTask(Task):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.database = DataBase()

    def run(self) -> Sequence[Table]:
        with self.database.session as session:
            return session.execute(self.query).scalars().all()

    def query(self) -> Select:
        raise NotImplementedError


class UpsertTask(Task):
    def __init__(self, model: Type[Table], conflict_columns: List[Col] = None, **kwargs: Any):
        self.database = DataBase()
        self.table_name = model.__table__
        self.model = model
        if conflict_columns is None:
            conflict_columns = [model.id]
        self.conflict_columns = conflict_columns
        super().__init__(**kwargs)

    def run(self, data: List[dict]) -> None:

        stmt = postgresql.insert(self.table_name).values(data)
        update_stmt = stmt.on_conflict_do_update(index_elements=self.conflict_columns, set_=stmt.excluded)
        self.database.engine.execute(update_stmt)
