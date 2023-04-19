from __future__ import annotations

import pathlib
import sys

import click

from n.app import App
from n.util import cd

NOTES = "NOTES"
EDITOR = "EDITOR"
DEFAULT_EDITOR = "vim"
FUZZY_THRESHOLD = 90


@click.group
@click.option("--path", "root", envvar=NOTES, type=pathlib.Path)
@click.option("--editor", "editor_name", envvar=EDITOR)
@click.pass_context
def cli(ctx: click.Context, root: pathlib.Path | None, editor_name: str | None):
    """
    n is a terminal-based notetaking system designed around speed and ease-of-use.
    """
    if not root or not root.exists() or not root.is_dir():
        raise ValueError(
            f"'{root}' is an invalid value for {NOTES}; please use an existing directory."
        )

    editor_name = editor_name or DEFAULT_EDITOR
    app = App.create(
        root=root, editor_name=editor_name, fuzzy_threshold=FUZZY_THRESHOLD
    )
    cd(root)
    ctx.obj = app


@cli.command(name="add")
@click.argument("name", nargs=1)
@click.option("-t", "--tag", "tags", multiple=True)
@click.pass_obj
def add_cmd(app: App, name: str, tags: tuple[str, ...]) -> None:
    """
    Create a new note.
    """
    app.add_note(name=name, tags=tags, fuzzy_match=True)


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
    app.grep_notes(args)


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
