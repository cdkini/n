from __future__ import annotations

from unittest import mock

import pytest

from n.fuzzy_matcher import FuzzyMatcher


@pytest.fixture
def threshold():
    return 90


@pytest.fixture
def fuzzy_matcher(threshold: int) -> FuzzyMatcher:
    return FuzzyMatcher(threshold=threshold)


@pytest.mark.parametrize(
    "name,candidates,expected",
    [
        pytest.param(
            "PyCon 2023",
            ["PyCon 2020", "PyCon Presentation"],
            ["PyCon 2020"],
            id="single match",
        ),
        pytest.param(
            "PyCon 2023",
            ["PyCon 2020", "PyCon 2022", "PyCon Presentation"],
            ["PyCon 2020", "PyCon 2022"],
            id="multiple matches",
        ),
        pytest.param(
            "PyCon 2023",
            ["PyCon Presentation", "Strange Loop"],
            [],
            id="no matches",
        ),
    ],
)
def test_determine_viable_candidates(
    fuzzy_matcher: FuzzyMatcher, name: str, candidates: list[str], expected: list[str]
) -> None:
    actual = fuzzy_matcher.determine_viable_candidates(name=name, candidates=candidates)
    assert expected == actual


def test_prompt_user_with_fuzzy_matches(fuzzy_matcher: FuzzyMatcher) -> None:
    name = "PyCon 2023"
    candidates = ["PyCon 2020", "PyCon 2022", "PyCon Presentation"]

    with mock.patch(
        f"{FuzzyMatcher.__module__}.{FuzzyMatcher.__name__}._prompt", return_value=1,
    ) as mock_prompt:
        match = fuzzy_matcher.prompt_user_with_fuzzy_matches(
            name=name, candidates=candidates
        )

    expected_text = "  1) PyCon 2023 (USER INPUT)\n  2) PyCon 2020\n  3) PyCon 2022\n"
    mock_prompt.assert_called_once_with(expected_text)
    assert match is None
