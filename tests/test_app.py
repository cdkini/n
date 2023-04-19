import pathlib
from typing import Callable

import pytest

from n.app import App
from n.editor import Editor
from n.fuzzy_matcher import FuzzyMatcher


@pytest.fixture
def root(tmp_path: pathlib.Path) -> pathlib.Path:
    d = tmp_path / "test_app"
    d.mkdir(exist_ok=True)
    return d


@pytest.fixture
def construct_app() -> Callable[[pathlib.Path, Editor, FuzzyMatcher], App]:
    def _construct_app(
        root: pathlib.Path, editor: Editor, fuzzy_matcher: FuzzyMatcher
    ) -> App:
        return App(root=root, editor=editor, fuzzy_matcher=fuzzy_matcher)

    return _construct_app


def test_add_note():
    pass


def test_open_note():
    pass


def test_open_daily_note():
    pass


def test_list_notes():
    pass


def test_delete_note():
    pass


def test_grep_notes():
    pass
