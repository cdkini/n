from __future__ import annotations

import pathlib
import subprocess

from n.frontmatter import YAMLFrontMatter


class App:

    DEFAULT_EDITOR = "vim"

    def __init__(self, root: pathlib.Path, editor: str) -> None:
        self._root = root
        self._editor = editor or App.DEFAULT_EDITOR

        notes = sorted(filter(lambda n: n.suffix == ".md", self._root.iterdir()))
        self._notes = {note.stem.lower(): note for note in notes}

    def add_note(self, name: str) -> None:
        path = self._root.joinpath(f"{name}.md")
        if path.exists():
            raise ValueError(f"'{name}' already exists.")

        yfm = YAMLFrontMatter(title=name)
        yfm_str = str(yfm)
        with path.open("w") as f:
            f.write(yfm_str)

        subprocess.call([self._editor, path.as_posix()])
        with path.open() as f:
            contents = f.read()

        # Don't save if no edits were made
        if contents == yfm_str:
            path.unlink()

    def list_notes(self) -> None:
        for name in self._notes:
            print(name)
