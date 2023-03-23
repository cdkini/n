from __future__ import annotations

from thefuzz import process


class FuzzyMatcher:
    def __init__(self, threshold: int) -> None:
        self._threshold = threshold

    def determine_candidates(self, name: str, items: list[str]) -> list[str]:
        candidates = process.extractBests(name.lower(), items)
        return [
            candidate for candidate, score in candidates if score >= self._threshold
        ]
