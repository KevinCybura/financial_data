build:
	poetry install

update:
	poetry update

test:
	poetry run pytest

fmt:
	poetry run isort .
	poetry run black .

createdb:
	createuser -s fin_data
	createdb fin_data

dropdb:
	dropdb --if-exists test_fin_data
	dropdb --if-exists fin_data
	dropuser --if-exists fin_data

migrate:
	poetry run alembic upgrade head

db: dropdb createdb


mypy:
	poetry run mypy financial_data --config-file mypy.ini

deploy-build:
	pip install toml && python -c 'import toml; c = toml.load("pyproject.toml"); \
	print("\n".join(c["build-system"]["requires"]))' | pip install -r /dev/stdin
