"""Reusable repository-status semantics for governed reference docs."""

from __future__ import annotations

REFERENCE_REPOSITORY_STATUS_PREFIXES = {
    "candidate_future_guidance": "Candidate reference.",
    "supporting_authority": "Supporting authority",
    "active_support": "Active support",
}

REFERENCE_REPOSITORY_STATUS_VALUES = tuple(REFERENCE_REPOSITORY_STATUS_PREFIXES)

__all__ = [
    "REFERENCE_REPOSITORY_STATUS_PREFIXES",
    "REFERENCE_REPOSITORY_STATUS_VALUES",
]
