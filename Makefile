build:
	poetry install

update:
	poetry update

test:
	poetry run pytest

fmt:
	isort .
	black .

prefect:
	prefect server start --postgres-port 5433 -d
	prefect agent local start -l iex-core-data --no-hostname-label --show-flow-logs

createdb:
	createuser -s fin_data
	createdb fin_data

dropdb:
	dropdb --if-exists test_fin_data
	dropdb --if-exists fin_data
	dropuser --if-exists fin_data

migrate:
	alembic upgrade head

db: dropdb createdb migrate

mypy:
	mypy financial_data --config-file mypy.ini

deploy-build:
	pip install toml && python -c 'import toml; c = toml.load("pyproject.toml"); \
	print("\n".join(c["build-system"]["requires"]))' | pip install -r /dev/stdin
