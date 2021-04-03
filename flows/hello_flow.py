import os
import time
import prefect
from prefect import task, Flow, Parameter
from prefect.run_configs import LocalRun
from prefect.executors import LocalDaskExecutor
from prefect.storage import Local


@task()
def say_hello(name):
    time.sleep(10)
    greeting = os.environ.get("GREETING")
    logger = prefect.context.get("logger")
    logger.info(f"{greeting}, {name}!")


with Flow(
    "hello-flow", storage=Local(stored_as_script=True, path="flows/hello_flow.py")
) as flow:
    people = Parameter("people", default=["Kevin", "Andrew", "Marvin"])
    say_hello.map(people)

flow.run_config = LocalRun(env={"GREETING": "Hello"}, labels=["kevincybura-X570-UD"])
flow.executor = LocalDaskExecutor()
