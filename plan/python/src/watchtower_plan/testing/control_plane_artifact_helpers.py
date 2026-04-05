"""Shared helpers for plan-owned control-plane artifact integration suites."""

from __future__ import annotations

from pathlib import Path

from watchtower_core.testing.fixtures import (
    FRONT_MATTER_PATTERN,
    load_front_matter,
    load_json_object,
)

REPO_ROOT = Path(__file__).resolve().parents[5]

__all__ = [
    "FRONT_MATTER_PATTERN",
    "REPO_ROOT",
    "load_front_matter",
    "load_json_object",
]
