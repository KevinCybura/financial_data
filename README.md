# Financial data pipelines

A [prefect](https://docs.prefect.io/) implementation for building data pipelines and performing ETL on financial data.

## Migrations
#### Running migrations
```bash
poetry run python manage.py migrate <APP_NAME>
```
#### Creating migrations
```bash
poetry run python manage.py makemigrations <APP_NAME> -m <MESSAGE>
```

#### If initial migration
1. append version path to `version_path` list in alembic.ini
```ini
version_locations = ...  %(here)s/financial_data/<YOUR_APP>/migrations 
```
2. run init the migrations using `init-migrations` in manage.py
```bash
poetry run python init-migrations <APP_NAME>
```
3. add script path to alembic.ini
```ini
[<APP_NAME>]
script_location = financial_data/<APP_NAME>/migrations
```
4. run initial migrations
```bash
python manage.py makemigrations <APP_NAME> -m <MESSAGE> -v <MIGRATIONS_DIR> -i
```

## Prefect notes

[Registering flows discussion on Prefect repo](https://github.com/PrefectHQ/prefect/discussions/4042)