from prefect import Task

from financial_data.db import PostgresSettings


class PostgresExecuteTask(Task):
    def __init__(
        self,
        database: str = None,
        user: str = None,
        password: str = None,
        host: str = None,
        port: int = None,
        query: str = None,
        data: tuple = None,
        commit: bool = False,
        **kwargs,
    ):
        self.database = PostgresSettings(database=database, user=user, password=password, host=host, port=port)

        self.query = query
        self.data = data
        self.commit = commit
        super().__init__(**kwargs)

    def run(self) -> None:
        pass
