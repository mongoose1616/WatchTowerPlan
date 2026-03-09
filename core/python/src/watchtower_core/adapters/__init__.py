"""Adapters for parsing and normalizing governed input surfaces."""

from watchtower_core.adapters.front_matter import FrontMatterParseError, load_front_matter

__all__ = [
    "FrontMatterParseError",
    "load_front_matter",
]
