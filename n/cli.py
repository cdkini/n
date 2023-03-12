from __future__ import annotations

import pathlib
import sys

import click

from n.app import App

NOTES = "NOTES"
EDITOR = "EDITOR"


@click.group
@click.option("--path", envvar=NOTES, type=pathlib.Path)
@click.option("--editor", envvar=EDITOR, default="vim")
@click.pass_context
def cli(ctx: click.Context, path: pathlib.Path | None, editor: str | None):
    if not path or not path.exists() or not path.is_dir():
        raise ValueError(
            f"'{path}' is an invalid value for {NOTES}; please use an existing directory."
        )
    ctx.obj = App(root=path, editor=editor)


@cli.command(name="add")
@click.argument("name", nargs=1)
@click.option("-t", "--tag", "tags", multiple=True)
@click.pass_obj
def add_cmd(app: App, name: str, tags: tuple[str, ...]) -> None:
    app.add_note(name=name, tags=tags)


@cli.command(name="open")
@click.argument("name", nargs=1)
@click.pass_obj
def open_cmd(app: App, name: str) -> None:
    app.open_note(name)


@cli.command(name="daily")
@click.pass_obj
def daily_cmd(app: App) -> None:
    app.open_daily_note()


@cli.command(name="grep")
@click.pass_obj
def grep_cmd(app: App) -> None:
    raise NotImplementedError()


@cli.command(name="list")
@click.pass_obj
def list_cmd(app: App) -> None:
    app.list_notes()


@cli.command(name="delete")
@click.argument("name", nargs=1)
@click.pass_obj
def delete_cmd(app: App, name: str) -> None:
    app.delete_note(name)


if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
