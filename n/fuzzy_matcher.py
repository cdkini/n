from __future__ import annotations

import click
from thefuzz import process


class FuzzyMatcher:
    def __init__(self, threshold: int) -> None:
        self._threshold = threshold

    def prompt_user_with_fuzzy_matches(
        self, name: str, candidates: list[str]
    ) -> str | None:
        viable_candidates = self._determine_viable_candidates(
            name=name, candidates=candidates
        )
        if not viable_candidates:
            return None

        print("Found similar existing notes; please pick which one you'd like to view:")
        selection = self._prompt_user_with_fuzzy_matches(
            name=name, candidates=viable_candidates
        )

        if selection == 1:
            return None
        return viable_candidates[selection - 2]

    def _determine_viable_candidates(
        self, name: str, candidates: list[str]
    ) -> list[str]:
        viable_candidates = process.extractBests(name.lower(), candidates)
        return [
            candidate
            for candidate, score in viable_candidates
            if score >= self._threshold
        ]

    def _prompt_user_with_fuzzy_matches(self, name: str, candidates: list[str]) -> int:
        text = self._construct_fuzzy_match_prompt(name=name, candidates=candidates)
        return int(
            click.prompt(
                text=text,
            )
        )

    def _construct_fuzzy_match_prompt(self, name: str, candidates: list[str]) -> str:
        text = f"  1) {name} (USER INPUT)\n"
        text += "\n".join(
            f"  {i}) {candidate}" for i, candidate in enumerate(candidates, 2)
        )
        text += "\n"
        return text
