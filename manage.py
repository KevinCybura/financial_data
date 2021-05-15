import os
import subprocess
from pathlib import Path
from typing import List
from typing import Optional

import click
from pydantic import BaseModel

env_py = """
from financial_data.config.env import run_migrations
from financial_data.{app}.models import {base_name}

run_migrations({base_name}.metadata, {base_name}.metadata.schema)
"""
mako_file = """

\"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

\"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}
    """


@click.group()
def cli():
    pass


@cli.command()
@click.argument("app")
def migrate(app):
    click.echo(f"Making initial migration for {app}...")
    args = ["alembic", f"--name={app}", "upgrade", f"{app}@head"]
    subprocess.run(args, text=True)


class MakeMigrations:
    def __init__(
        self, app: str, version_path: Optional[str] = None, message: Optional[str] = None, initial: bool = False
    ):
        self.app = app
        self._version_path = version_path
        self.initial = initial
        self._message = message
        if self._message:
            self._message = f"--message='{message}'"

        self.base_args = ["alembic", f"--name={app}", "revision"]

    @property
    def message(self) -> str:
        return self._message

    def args(self):
        args = self.base_args

        if self.message:
            args += [self.message]

        if self.initial:
            args += self.initial_args()
        else:
            args += [f"--head={self.app}@base"]

        args += ["--autogenerate"]

        return args

    def initial_args(self) -> List[str]:
        version_path = self._version_path
        if not self._version_path:
            version_path = f"financial_data/{self.app}/migrations/versions"

        if not os.path.exists(version_path):
            click.echo(
                click.style(f"Making versions directory for app={self.app}, path={version_path}...", fg="yellow")
            )
            os.makedirs(f"./{version_path}")

        return ["--head=base", f"--branch-label={self.app}", f"--version-path={version_path}"]


@cli.command()
@click.argument("app")
@click.option("--version-path", "-v", help="path to versions directory")
@click.option("--message", "-m", help="name of the migration")
@click.option("--initial", "-i", is_flag=True, help="initial migration")
def makemigrations(app, version_path, message, initial):
    cmd = MakeMigrations(app=app, version_path=version_path, message=message, initial=initial)
    migrations_message = f"Making migration for {app}..."
    if initial:
        migrations_message = f"Making initial migration for {app}..."

    click.echo(click.style(migrations_message, fg="green"))

    # Run command.
    output = subprocess.run(cmd.args(), text=True, capture_output=True)

    result_message = click.style(output.stdout, fg="green", bold=True)
    if output.returncode != 0:
        result_message = click.style(output.stderr, fg="red", bold=True)

    click.echo(result_message)


class File(BaseModel):
    name: str
    file_name: str
    path: Path
    contents: Optional[str]
    is_dir: Optional[bool] = False

    def __str__(self) -> str:
        return f"name={self.name}, path={self.path / self.file_name}"

    def create(self) -> bool:
        if self.exists():
            return False

        if self.is_dir:
            os.makedirs(self.path)
        else:
            with open(self.path / self.file_name, "w") as f:
                if self.contents:
                    f.write(self.contents)

        return True

    def exists(self) -> bool:
        if self.is_dir:
            return os.path.exists(self.path)

        return os.path.exists(self.path / self.file_name)


@cli.command()
@click.argument("app")
@click.option("--base-name", "-n", help="Name of declarative base defaults to <App>Base")
def init_migrations(app, base_name):
    click.echo(click.style(f"Initializing migrations for app={app}", fg="green", bold=True))

    if not base_name:
        base_name = f"{app.title()}Base"

    env = env_py.format(app=app, base_name=base_name)

    migrations_path = Path(f"financial_data/{app}/migrations")

    files = [
        File(name="migrations", file_name="migrations", path=migrations_path, is_dir=True),
        File(name="init", file_name="__init__.py", path=migrations_path),
        File(name="env", file_name="env.py", path=migrations_path, contents=env),
        File(name="mako script", file_name="script.py.mako", path=migrations_path, contents=mako_file),
    ]

    for file in files:
        try:
            if file.create():
                click.echo(click.style(f"    Creating {file}", fg="green"))
            else:
                click.echo(click.style(f"    File already exists {file}", fg="yellow"))
        except Exception as e:
            click.echo(click.style(str(e), fg="red"))


if __name__ == "__main__":
    cli()
