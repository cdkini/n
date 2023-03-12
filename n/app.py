from __future__ import annotations

import datetime as dt
import pathlib
import subprocess

from n.frontmatter import YAMLFrontMatter


class App:

    DEFAULT_EDITOR = "vim"

    def __init__(self, root: pathlib.Path, editor: str | None) -> None:
        self._root = root
        self._editor = editor or App.DEFAULT_EDITOR

    def add_note(self, name: str, tags: tuple[str, ...]) -> None:
        path = self._build_note_path(name)
        if path.exists():
            raise ValueError(f"'{name}' already exists.")

        yfm = YAMLFrontMatter(title=name, tags=tags)
        with path.open("w") as f:
            f.write(str(yfm))

        self._open_with_editor(path)
        with path.open() as f:
            contents = f.read()
            # Don't save if no edits were made
            if contents == yfm:
                path.unlink()

    def open_note(self, name: str) -> None:
        path = self._build_note_path(name)
        if not path.exists():
            raise ValueError(f"'{name}' does not exist.")
        self._open_with_editor(path)

    def open_daily_note(self) -> None:
        name = dt.date.today().isoformat()
        path = self._build_note_path(name)
        if path.exists():
            self.open_note(name)
        else:
            self.add_note(name=name, tags=("daily",))

    def list_notes(self) -> None:
        notes = sorted(filter(lambda n: n.suffix == ".md", self._root.iterdir()))
        for note in notes:
            print(note.stem)

    def delete_note(self, name: str) -> None:
        path = self._build_note_path(name)
        try:
            path.unlink(missing_ok=False)
        except FileNotFoundError:
            raise ValueError(f"'{name}' does not exist.")

    def _build_note_path(self, name: str) -> pathlib.Path:
        return self._root.joinpath(f"{name}.md")

    def _open_with_editor(self, path: pathlib.Path):
        subprocess.call([self._editor, path.as_posix()])
