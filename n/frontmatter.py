from __future__ import annotations

import datetime as dt


class YAMLFrontMatter:
    def __init__(self, title: str, tags: list[str] | None = None) -> None:
        self._title = title
        self._tags = tags or []
        self._date = dt.date.today().isoformat()

    def __str__(self) -> str:
        contents = []
        contents.append("---")
        contents.append(f"title: {self._title}")
        contents.append(f"date: {self._date}")
        contents.append(f"tags: {','.join(tag for tag in self._tags)}")
        contents.append("---")
        return "\n".join(c for c in contents)
