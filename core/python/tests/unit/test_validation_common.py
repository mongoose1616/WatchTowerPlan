from __future__ import annotations

from watchtower_core.validation.common import matches_applies_to


def test_matches_applies_to_supports_generic_hosted_pack_reference_roots() -> None:
    assert matches_applies_to(
        "packs/fixture/docs/references/example_reference.md",
        "packs/*/docs/references/**",
    )
    assert matches_applies_to(
        "packs/fixture/docs/references/nested/example_reference.md",
        "packs/*/docs/references/**",
    )


def test_matches_applies_to_supports_top_level_pack_reference_roots() -> None:
    assert matches_applies_to(
        "alpha/docs/references/example_reference.md",
        "*/docs/references/**",
    )
    assert matches_applies_to(
        "alpha/docs/references/nested/example_reference.md",
        "*/docs/references/**",
    )
    assert matches_applies_to(
        "alpha/docs/references",
        "*/docs/references/**",
    )


def test_matches_applies_to_rejects_unrelated_paths() -> None:
    assert not matches_applies_to(
        "alpha/docs/standards/example_standard.md",
        "*/docs/references/**",
    )
