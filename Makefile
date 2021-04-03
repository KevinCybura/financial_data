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

deploy-build:
	pip install toml && python -c 'import toml; c = toml.load("pyproject.toml"); \
	print("\n".join(c["build-system"]["requires"]))' | pip install -r /dev/stdin
