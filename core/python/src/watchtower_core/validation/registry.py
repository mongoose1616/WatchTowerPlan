"""Canonical registry for aggregate validation families."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationFamilySpec:
    """One validation family included in aggregate validation."""

    family: str
    runner_name: str
    cli_skip_attr: str


VALIDATION_FAMILY_SPECS: tuple[ValidationFamilySpec, ...] = (
    ValidationFamilySpec(
        family="front_matter",
        runner_name="_validate_front_matter",
        cli_skip_attr="skip_front_matter",
    ),
    ValidationFamilySpec(
        family="document_semantics",
        runner_name="_validate_document_semantics",
        cli_skip_attr="skip_document_semantics",
    ),
    ValidationFamilySpec(
        family="artifacts",
        runner_name="_validate_artifacts",
        cli_skip_attr="skip_artifacts",
    ),
    ValidationFamilySpec(
        family="acceptance",
        runner_name="_validate_acceptance",
        cli_skip_attr="skip_acceptance",
    ),
)


__all__ = ["VALIDATION_FAMILY_SPECS", "ValidationFamilySpec"]
