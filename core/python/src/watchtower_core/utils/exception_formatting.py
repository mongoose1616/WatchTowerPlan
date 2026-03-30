"""Small helpers for stable human-readable exception details."""

from __future__ import annotations


def format_exception_detail(exc: BaseException) -> str:
    """Return one stable detail string including the exception type."""

    message = str(exc)
    if message:
        return f"{type(exc).__name__}: {message}"
    return type(exc).__name__


__all__ = ["format_exception_detail"]
