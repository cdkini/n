from __future__ import annotations

import pathlib
import sys

import click

from n.app import App
from n.editor import Editor

NOTES = "NOTES"
EDITOR = "EDITOR"


@click.group
@click.option("--path", envvar=NOTES, type=pathlib.Path)
@click.option("--editor", envvar=EDITOR, default="vim")
@click.pass_context
def cli(ctx: click.Context, path: pathlib.Path | None, editor: str | None):
    """
    n is a terminal-based notetaking system designed around speed and ease-of-use.
    """
    if not path or not path.exists() or not path.is_dir():
        raise ValueError(
            f"'{path}' is an invalid value for {NOTES}; please use an existing directory."
        )
    ctx.obj = App(root=path, editor=Editor(editor))


@cli.command(name="add")
@click.argument("name", nargs=1)
@click.option("-t", "--tag", "tags", multiple=True)
@click.pass_obj
def add_cmd(app: App, name: str, tags: tuple[str, ...]) -> None:
    """
    Create a new note.
    """
    app.add_note(name=name, tags=tags)


@cli.command(name="open")
@click.argument("name", nargs=1)
@click.pass_obj
def open_cmd(app: App, name: str) -> None:
    """
    Open existing notes.
    """
    app.open_note(name)


@cli.command(name="daily")
@click.pass_obj
def daily_cmd(app: App) -> None:
    """
    Open your daily note.
    """
    app.open_daily_note()


@cli.command(
    "grep", context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)
)
@click.argument("args", nargs=-1)
@click.pass_obj
def grep_cmd(app: App, args: tuple[str, ...]) -> None:
    """
    Search through notes with ripgrep.
    """
    app.grep(args)


@cli.command(name="list")
@click.pass_obj
def list_cmd(app: App) -> None:
    """
    List notes.
    """
    app.list_notes()


@cli.command(name="delete")
@click.argument("name", nargs=1)
@click.pass_obj
def delete_cmd(app: App, name: str) -> None:
    """
    Delete notes.
    """
    app.delete_note(name)


def main() -> None:
    try:
        cli()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
