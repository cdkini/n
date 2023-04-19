from __future__ import annotations

import datetime as dt
import pathlib

from n.editor import Editor
from n.frontmatter import YAMLFrontMatter
from n.fuzzy_matcher import FuzzyMatcher
from n.util import grep


class App:
    def __init__(
        self, root: pathlib.Path, editor: Editor, fuzzy_matcher: FuzzyMatcher
    ) -> None:
        self._root = root
        self._editor = editor
        self._fuzzy_matcher = fuzzy_matcher

    @classmethod
    def create(cls, root: pathlib.Path, editor_name: str, fuzzy_threshold: int) -> App:
        editor = Editor(editor_name)
        fuzzy_matcher = FuzzyMatcher(fuzzy_threshold)
        return cls(root=root, editor=editor, fuzzy_matcher=fuzzy_matcher)

    def add_note(self, name: str, tags: tuple[str, ...], fuzzy_match: bool) -> None:
        path = self._build_note_path(name)
        if path.exists():
            raise ValueError(f"'{name}' already exists.")

        existing_note = self._retrieve_note_if_exists(
            name=name, fuzzy_match=fuzzy_match
        )
        if existing_note:
            return self.open_note(existing_note)

        self._construct_note(path=path, name=name, tags=tags)

    def open_note(self, name: str) -> None:
        path = self._build_note_path(name)
        if not path.exists():
            raise ValueError(f"'{name}' does not exist.")
        self._editor.open(path)

    def open_daily_note(self) -> None:
        name = dt.date.today().isoformat()
        try:
            self.open_note(name)
        except ValueError:
            self.add_note(name=name, tags=("daily",), fuzzy_match=False)

    def list_notes(self) -> None:
        notes = self._collect_notes()
        for note in notes:
            print(note.stem)

    def delete_note(self, name: str) -> None:
        path = self._build_note_path(name)
        try:
            path.unlink(missing_ok=False)
        except FileNotFoundError:
            raise ValueError(f"'{name}' does not exist.")

    def grep_notes(self, args: tuple[str, ...]) -> None:
        grep(target=self._root, args=args)

    def _retrieve_note_if_exists(self, name: str, fuzzy_match: bool) -> str | None:
        notes = self._collect_notes()
        note_names = list(map(lambda n: n.stem, notes))
        if name in note_names:
            return name

        if fuzzy_match:
            return self._fuzzy_matcher.prompt_user_with_fuzzy_matches(
                name=name, candidates=note_names
            )
        return None

    def _construct_note(
        self, path: pathlib.Path, name: str, tags: tuple[str, ...]
    ) -> None:
        yfm = YAMLFrontMatter(title=name, tags=tags)
        with path.open("w") as f:
            f.write(str(yfm))
        self._editor.open(path)
        with path.open() as f:
            contents = f.read()
            # Don't save if no edits were made
            if contents == yfm:
                path.unlink()

    def _collect_notes(self) -> list[pathlib.Path]:
        return sorted(filter(lambda n: n.suffix == ".md", self._root.iterdir()))

    def _build_note_path(self, name: str) -> pathlib.Path:
        return self._root.joinpath(f"{name}.md")
