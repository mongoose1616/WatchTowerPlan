"""Shared helpers for index-backed query services."""

from __future__ import annotations

from collections.abc import Iterable


def normalize_text(value: str) -> str:
    """Normalize text for case-insensitive matching."""
    return value.casefold().strip()


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
