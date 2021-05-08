build:
	poetry install

update:
	poetry update

test:
	poetry run pytest

fmt:
	poetry run isort .
	poetry run black .

prefect-server:
	poetry run prefect server start --postgres-port 5433 -d

prefect-agent:
	poetry run prefect agent local start -l iex-data --no-hostname-label --show-flow-logs

createdb:
	createuser -s fin_data
	createdb fin_data

dropdb:
	dropdb --if-exists test_fin_data
	dropdb --if-exists fin_data
	dropuser --if-exists fin_data

migrate:
	poetry run alembic upgrade head

db: dropdb createdb migrate

mypy:
	poetry run mypy financial_data flows --config-file mypy.ini

deploy-build:
	pip install toml && python -c 'import toml; c = toml.load("pyproject.toml"); \
	print("\n".join(c["build-system"]["requires"]))' | pip install -r /dev/stdin
