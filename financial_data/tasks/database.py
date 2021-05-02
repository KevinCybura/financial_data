from typing import List
from typing import Type

from prefect.tasks.postgres import PostgresExecute
from sqlalchemy import Table
from sqlalchemy.dialects import postgresql

from financial_data.db import DataBase
from financial_data.db import PostgresSettings
from financial_data.tasks import Task
from financial_data.types import Col


# WIP
class PostgresTask(PostgresExecute):
    def __init__(self, model: Type[Table], conflict_columns: List[Col] = None, **kwargs):
        self.settings = PostgresSettings()
        query = self.build_query(model, kwargs.pop("data"), conflict_columns)
        super().__init__(query=query, **self.settings.dict(), **kwargs)

    def build_query(self, model: Type[Table], data: List[Table], conflict_columns: List[Col]):
        if conflict_columns is None:
            conflict_columns = [model.id]

        stmt = postgresql.insert(model.__table__).values(data)
        update_stmt = stmt.on_conflict_do_update(index_elements=[conflict_columns], set_=stmt.excluded)
        return update_stmt


class UpsertTask(Task):
    def __init__(self, model: Type[Table], conflict_columns: List[Col] = None, **kwargs):
        self.database = DataBase()
        self.table_name = model.__table__
        self.model = model
        if conflict_columns is None:
            conflict_columns = [model.id]
        self.conflict_columns = conflict_columns
        super().__init__(**kwargs)

    def run(self, data: List[dict]):
        stmt = postgresql.insert(self.table_name).values(data)
        update_stmt = stmt.on_conflict_do_update(index_elements=self.conflict_columns, set_=stmt.excluded)
        self.database.engine.execute(update_stmt)
