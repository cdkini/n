from __future__ import annotations

import datetime as dt


class YAMLFrontMatter:
    def __init__(self, title: str, tags: tuple[str, ...]) -> None:
        self._title = title
        self._tags = tags
        self._date = dt.date.today().isoformat()

    def __str__(self) -> str:
        contents = [
            "---",
            f"title: {self._title}",
            f"date: {self._date}",
            "category: ",
            f"tags: {', '.join(tag for tag in self._tags)}",
            "---",
            "\n\n",
        ]
        return "\n".join(contents)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, str):
            return str(self) == __o
        return super().__eq__(__o)
