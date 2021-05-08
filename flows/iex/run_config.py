import os
from typing import List

from prefect.run_configs import DockerRun
from prefect.run_configs import LocalRun
from prefect.run_configs import RunConfig


def reference_data_config(labels: List[str]) -> RunConfig:
    if os.environ.get("RUN_ENVIRONMENT", "local") == "local":
        return LocalRun(labels=labels)

    return DockerRun(image="financial-data:latest")
