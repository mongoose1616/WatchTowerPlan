"""Shared helpers for reusable-core query services."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import asdict
from typing import Any, cast


class DataclassSearchAdapter[ParamsT, TargetParamsT, EntryT]:
    """Translate one query dataclass into an adjacent typed search contract."""

    def __init__(
        self,
        *,
        target_type: type[TargetParamsT],
        search: Callable[[TargetParamsT], tuple[EntryT, ...]],
    ) -> None:
        self._target_type = target_type
        self._search = search

    def search(self, params: ParamsT) -> tuple[EntryT, ...]:
        """Delegate one query through a differently typed workspace contract."""

        payload = asdict(cast(Any, params))
        return self._search(self._target_type(**payload))


def normalize_text(value: str) -> str:
    """Normalize text for case-insensitive matching."""

    return value.casefold().strip()


def normalize_optional_text(value: str | None) -> str | None:
    """Normalize optional text for case-insensitive matching."""

    if value is None:
        return None
    return normalize_text(value)


def query_score(query: str | None, fields: Iterable[str]) -> int | None:
    """Return a simple relevance score or None when the query does not match."""

    if query is None:
        return 0

    tokens = [token for token in normalize_text(query).split() if token]
    if not tokens:
        return 0

    haystacks = [normalize_text(field) for field in fields if field]
    score = 0

    for token in tokens:
        token_score = 0
        for haystack in haystacks:
            if haystack == token:
                token_score = max(token_score, 12)
            elif haystack.startswith(token):
                token_score = max(token_score, 8)
            elif token in haystack:
                token_score = max(token_score, 4)
        if token_score == 0:
            return None
        score += token_score

    return score


__all__ = ["DataclassSearchAdapter", "normalize_optional_text", "normalize_text", "query_score"]
