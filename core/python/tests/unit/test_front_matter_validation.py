from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.pack_fixture_support import (
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation import FrontMatterValidationService, ValidationSelectionError

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_front_matter_validation_auto_selects_standard_validator() -> None:
    service = FrontMatterValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate("core/docs/standards/metadata/front_matter_standard.md")

    assert result.passed is True
    assert result.validator_id == "validator.documentation.standard_front_matter"
    assert result.issue_count == 0


def test_front_matter_validation_auto_selects_foundation_validator() -> None:
    service = FrontMatterValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate("core/docs/foundations/repository_scope.md")

    assert result.passed is True
    assert result.validator_id == "validator.documentation.foundation_front_matter"
    assert result.issue_count == 0


def test_front_matter_validation_rejects_unsupported_path_without_validator() -> None:
    service = FrontMatterValidationService(ControlPlaneLoader(REPO_ROOT))

    with pytest.raises(ValidationSelectionError):
        service.validate("core/docs/commands/core_python/watchtower_core.md")


def test_front_matter_validation_reports_missing_front_matter(tmp_path: Path) -> None:
    document_path = tmp_path / "missing_front_matter.md"
    document_path.write_text("# Missing front matter\n", encoding="utf-8")
    service = FrontMatterValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate(
        document_path,
        validator_id="validator.documentation.standard_front_matter",
    )

    assert result.passed is False
    assert result.issue_count == 1
    assert result.issues[0].code == "front_matter_missing"


def test_front_matter_validation_prefers_more_specific_pack_validator(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    surfaces = materialize_pack_validation_suite(
        repo_root / "packs" / "targets",
        pack_slug="targets",
        registry_mode="replace_default",
        default_repo_pack=True,
    )
    validator_registry_path = (
        repo_root / "packs" / "targets" / ".wt" / "registries" / "validator_registry.json"
    )
    validator_registry = json.loads(validator_registry_path.read_text(encoding="utf-8"))
    validator_registry["validators"].append(
        {
            "id": "validator.packs.targets_reference_front_matter",
            "title": "Targets Reference Front Matter Validator",
            "description": "Validates pack-owned reference docs for the targets fixture.",
            "status": "active",
            "engine": "json_schema",
            "artifact_kind": "documentation_front_matter",
            "applies_to": [
                "packs/targets/docs/references/*.md"
            ],
            "schema_ids": [
                "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1"
            ],
        }
    )
    validator_registry_path.write_text(
        json.dumps(validator_registry, indent=2) + "\n",
        encoding="utf-8",
    )

    target_path = repo_root / "packs" / "targets" / "docs" / "references" / "example_reference.md"
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(
        (REPO_ROOT / "core" / "docs" / "references" / "commonmark_reference.md").read_text(
            encoding="utf-8"
        ),
        encoding="utf-8",
    )

    service = FrontMatterValidationService(
        ControlPlaneLoader(
            repo_root=repo_root,
            active_pack_settings_path=surfaces["pack_settings_path"],
        )
    )

    result = service.validate("packs/targets/docs/references/example_reference.md")

    assert result.passed is True
    assert result.validator_id == "validator.packs.targets_reference_front_matter"
