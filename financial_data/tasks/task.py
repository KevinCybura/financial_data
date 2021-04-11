from prefect import Task

from financial_data.db import DataBase


class PostgresExecuteTask(Task):
    def __init__(
        self,
        query: str = None,
        data: tuple = None,
        commit: bool = False,
        **kwargs,
    ):
        self.database = DataBase()

        self.query = query
        self.data = data
        self.commit = commit
        super().__init__(**kwargs)

    def run(self) -> None:
        pass
