from __future__ import annotations

import datetime as dt
import pathlib
import subprocess

import click
from thefuzz import process

from n.editor import Editor
from n.frontmatter import YAMLFrontMatter


class App:

    GREP = "rg"
    FUZZ_THRESHOLD = 90

    def __init__(self, root: pathlib.Path, editor: Editor) -> None:
        self._root = root
        self._editor = editor

    def add_note(self, name: str, tags: tuple[str, ...]) -> None:
        path = self._build_note_path(name)
        if path.exists():
            raise ValueError(f"'{name}' already exists.")

        existing_note = self._fuzzy_match_existing_notes(name)
        if existing_note:
            return self.open_note(existing_note)

        yfm = self._add_frontmatter(path=path, name=name, tags=tags)
        self._editor.open(path)
        with path.open() as f:
            contents = f.read()
            # Don't save if no edits were made
            if contents == yfm:
                path.unlink()

    @staticmethod
    def _add_frontmatter(
        path: pathlib.Path, name: str, tags: tuple[str, ...]
    ) -> YAMLFrontMatter:
        yfm = YAMLFrontMatter(title=name, tags=tags)
        with path.open("w") as f:
            f.write(str(yfm))
        return yfm

    def _fuzzy_match_existing_notes(self, name: str) -> str | None:
        notes = self._collect_notes()
        candidates = process.extractBests(name.lower(), notes)
        viable_candidates = [
            candidate.stem
            for candidate, score in candidates
            if score >= App.FUZZ_THRESHOLD
        ]
        if not viable_candidates:
            return None

        print("Found similar existing notes; please pick which one you'd like to view:")
        text = self._construct_fuzzy_match_prompt(
            name=name, candidates=viable_candidates
        )
        selection = int(
            click.prompt(
                text=text,
            )
        )

        if selection == 1:
            return None
        return viable_candidates[selection - 2]

    @staticmethod
    def _construct_fuzzy_match_prompt(name: str, candidates: list[str]) -> str:
        text = f"  1) {name} (USER INPUT)\n"
        text += "\n".join(
            f"  {i}) {candidate}" for i, candidate in enumerate(candidates, 2)
        )
        text += "\n"
        return text

    def open_note(self, name: str) -> None:
        path = self._build_note_path(name)
        if not path.exists():
            raise ValueError(f"'{name}' does not exist.")
        self._editor.open(path)

    def open_daily_note(self) -> None:
        name = dt.date.today().isoformat()
        path = self._build_note_path(name)
        if path.exists():
            self.open_note(name)
        else:
            self.add_note(name=name, tags=("daily",))

    def list_notes(self) -> None:
        notes = self._collect_notes()
        for note in notes:
            print(note.stem)

    def _collect_notes(self) -> list[pathlib.Path]:
        return sorted(filter(lambda n: n.suffix == ".md", self._root.iterdir()))

    def delete_note(self, name: str) -> None:
        path = self._build_note_path(name)
        try:
            path.unlink(missing_ok=False)
        except FileNotFoundError:
            raise ValueError(f"'{name}' does not exist.")

    def grep(self, args: tuple[str, ...]) -> None:
        command = [App.GREP]
        for arg in args:
            command.append(arg)
        command.append(self._root.as_posix())
        subprocess.call(command)

    def _build_note_path(self, name: str) -> pathlib.Path:
        return self._root.joinpath(f"{name}.md")
