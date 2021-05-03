import os
import time

import prefect
from prefect import Flow
from prefect import Parameter
from prefect import task
from prefect.executors import LocalDaskExecutor
from prefect.run_configs import LocalRun
from prefect.storage import Local


@task()
def say_hello(name: str) -> None:
    time.sleep(10)
    greeting = os.environ.get("GREETING")
    logger = prefect.context.get("logger")
    logger.info(f"{greeting}, {name}!")


with Flow("hello-flow", storage=Local(stored_as_script=True, path="flows/hello_flow.py")) as flow:
    people = Parameter("people", default=["Kevin", "Andrew", "Marvin"])
    say_hello.map(people)

flow.run_config = LocalRun(env={"GREETING": "Hello"}, labels=["kevincybura-X570-UD"])
flow.executor = LocalDaskExecutor()
