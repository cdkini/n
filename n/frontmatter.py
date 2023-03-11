import datetime as dt

class YAMLFrontMatter:
    def __init__(self, title: str) -> None:
        self._title = title.title()
        self._date = dt.date.today().isoformat()

    def __str__(self) -> str:
        contents = []
        contents.append("---")
        contents.append(f"title: {self._title}")
        contents.append(f"date: {self._date}")
        contents.append("---")
        return "\n".join(c for c in contents)
