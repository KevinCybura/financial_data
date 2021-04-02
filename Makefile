build:
	poetry install

update:
	poetry update

test:
	poetry run pytest

fmt:
	poetry run isort .
	poetry run black .

mypy:
	poetry run mypy financial_data
