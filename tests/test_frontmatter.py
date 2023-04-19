from __future__ import annotations

import datetime as dt

import pytest

from n.frontmatter import YAMLFrontMatter


@pytest.mark.parametrize(
    "title,tags,date,expected",
    [
        pytest.param(
            "Meeting Minutes 2023-02-12",
            ("work", "meeting_minutes"),
            dt.date(2023, 2, 12),
            "---\ntitle: Meeting Minutes 2023-02-12\ndate: 2023-02-12\ntags: work, meeting_minutes\n---\n\n\n",
            id="with tags",
        ),
        pytest.param(
            "Meeting Minutes 2023-02-12",
            (),
            dt.date(2023, 2, 12),
            "---\ntitle: Meeting Minutes 2023-02-12\ndate: 2023-02-12\ntags: \n---\n\n\n",
            id="no tags",
        ),
    ],
)
def test_frontmatter___str__(
    title: str, tags: tuple[str, ...], date: dt.datetime, expected: str
) -> None:
    frontmatter = YAMLFrontMatter(title=title, tags=tags, date=date)
    assert str(frontmatter) == expected


def test_frontmatter___eq__() -> None:
    title = "Architecture Review"
    tags = ("work",)
    date = dt.datetime(2023, 1, 1)

    frontmatter = YAMLFrontMatter(title=title, tags=tags, date=date)
    string = "---\ntitle: Architecture Review\ndate: 2023-01-01T00:00:00\ntags: work\n---\n\n\n"

    assert frontmatter == string
