import os
from typing import List

from prefect.run_configs import DockerRun
from prefect.run_configs import LocalRun
from prefect.run_configs import RunConfig

from financial_data.config import common


def reference_data_config(labels: List[str]) -> RunConfig:
    if common.ENVIRONMENT is common.EnvType.LOCAL:
        return LocalRun(labels=labels)

    return DockerRun(image="financial-data:latest")
