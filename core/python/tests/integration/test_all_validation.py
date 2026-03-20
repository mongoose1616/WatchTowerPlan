from __future__ import annotations

import json
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from shutil import copytree
from textwrap import dedent
from typing import Any

import pytest

from tests.fixture_repo_support import (
    materialize_acceptance_and_evidence_paths,
    materialize_minimal_plan_pack,
)
from watchtower_core.control_plane.loader import (
    VALIDATOR_REGISTRY_PATH,
    ControlPlaneLoader,
)
from watchtower_core.validation.pack_targets import (
    resolve_pack_validation_suite_targets,
)
from watchtower_core.validation.all import VALIDATION_ALL_FAMILIES, ValidationAllService
from watchtower_core.validation.errors import ValidationSelectionError
from watchtower_core.validation.front_matter import FrontMatterValidationService
from watchtower_plan.sync.reference_index import ReferenceIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def _copy_control_plane_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    materialize_minimal_plan_pack(repo_root, REPO_ROOT)
    materialize_acceptance_and_evidence_paths(repo_root, REPO_ROOT)
    return repo_root


def _service(repo_root: Path | None = None) -> ValidationAllService:
    return ValidationAllService(
        ControlPlaneLoader(repo_root),
        suite_id="suite.plan.validation_baseline",
        suite_target_resolver=resolve_pack_validation_suite_targets,
    )


def _service_with_targets(
    step_targets: dict[str, tuple[str, ...]],
    repo_root: Path | None = None,
) -> ValidationAllService:
    def resolver(_, step) -> tuple[str, ...] | None:
        return step_targets.get(step.step_id, ())

    return ValidationAllService(
        ControlPlaneLoader(repo_root),
        suite_id="suite.plan.validation_baseline",
        suite_target_resolver=resolver,
    )


def _write_invalid_standard_fixture(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        dedent(
            """\
            ---
            id: "std.documentation.validate_all_standard_semantics"
            title: "Validate All Standard Semantics"
            summary: "Exercises aggregate validation for governed standard semantics."
            type: standard
            status: active
            tags:
              - "standard"
              - "documentation"
              - "example"
            owner: repository_maintainer
            updated_at: "2026-03-11T17:05:00Z"
            audience: shared
            authority: authoritative
            ---

            # Validate All Standard Semantics

            ## Summary
            Exercises aggregate validation for governed standard semantics.

            ## Purpose
            Keep the aggregate validator aligned with standard semantics.

            ## Scope
            - Applies to one invalid standard fixture.

            ## Use When
            - Added to pin validate-all coverage.

            ## Related Standards and Sources
            - [validate_all_standard_semantics.md](/core/docs/standards/documentation/validate_all_standard_semantics.md): keeps the fixture self-contained while exercising missing-section validation.

            ## Operationalization
            - `Modes`: `documentation`
            - `Operational Surfaces`: `core/docs/standards/documentation/validate_all_standard_semantics.md`

            ## Validation
            - Validate-all should surface the missing Guidance section directly.

            ## Change Control
            - Update the validator and fixture together if the required sections change.

            ## References
            - [validate_all_standard_semantics.md](/core/docs/standards/documentation/validate_all_standard_semantics.md)

            ## Updated At
            - `2026-03-11T17:05:00Z`
            """
        ),
        encoding="utf-8",
    )


def test_validate_all_can_pass_when_acceptance_is_skipped() -> None:
    service = _service()

    result = service.run(
        included_families=tuple(
            family for family in VALIDATION_ALL_FAMILIES if family != "acceptance"
        )
    )

    assert result.passed is True
    assert result.total_count >= 1
    assert result.failed_count == 0
    assert result.included_families == tuple(
        family for family in VALIDATION_ALL_FAMILIES if family != "acceptance"
    )
    assert any(summary.family == "pack_contract" for summary in result.family_summaries)
    assert any(summary.family == "front_matter" for summary in result.family_summaries)
    assert any(summary.family == "document_semantics" for summary in result.family_summaries)
    assert any(summary.family == "artifacts" for summary in result.family_summaries)


def test_validate_all_passes_when_all_governed_families_are_aligned() -> None:
    service = _service()

    result = service.run()

    assert result.passed is True
    assert result.total_count >= 1
    assert result.failed_count == 0
    assert result.included_families == VALIDATION_ALL_FAMILIES
    acceptance_summary = next(
        summary for summary in result.family_summaries if summary.family == "acceptance"
    )
    assert acceptance_summary.total_count >= 1
    assert acceptance_summary.failed_count == 0


def test_validation_family_registry_is_unique() -> None:
    assert len(set(VALIDATION_ALL_FAMILIES)) == len(VALIDATION_ALL_FAMILIES)


def test_validate_all_rejects_unknown_family() -> None:
    service = _service()

    with pytest.raises(ValueError, match="unknown validation families: imaginary"):
        service.run(included_families=("imaginary",))


def test_validate_all_requires_at_least_one_selected_family() -> None:
    service = _service()

    with pytest.raises(ValueError, match="requires at least one validation family"):
        service.run(included_families=())


def test_validate_all_records_selection_errors_as_failed_results(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = "core/docs/references/example_reference.md"
    service = _service_with_targets(
        {"step.plan.front_matter": (target,)},
    )

    def raise_selection_error(
        self: FrontMatterValidationService,
        relative_path: str,
        *,
        validator_id: str | None = None,
    ) -> object:
        raise ValidationSelectionError(f"No validator matched {relative_path}")

    monkeypatch.setattr(FrontMatterValidationService, "validate", raise_selection_error)

    result = service.run(included_families=("front_matter",))

    assert result.passed is False
    assert result.failed_count == 1
    assert result.records[0].family == "front_matter"
    assert result.records[0].target == target
    assert result.records[0].result.validator_id == "suite:front_matter:auto"
    assert result.records[0].result.issue_count == 1
    assert result.records[0].result.issues[0].code == "validation_step_error"


def test_validate_all_reports_missing_standard_guidance_section(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    relative_path = "core/docs/standards/documentation/validate_all_standard_semantics.md"
    _write_invalid_standard_fixture(repo_root / relative_path)
    service = _service_with_targets(
        {"step.plan.document_semantics": (relative_path,)},
        repo_root,
    )

    result = service.run(included_families=("document_semantics",))

    assert result.passed is False
    assert result.failed_count == 1
    assert result.records[0].family == "document_semantics"
    assert result.records[0].target == relative_path
    assert result.records[0].result.validator_id == "validator.documentation.standard_semantics"
    assert "missing required sections: Guidance" in result.records[0].result.issues[0].message


def test_validate_all_artifacts_include_live_control_plane_targets() -> None:
    service = _service()

    result = service.run(included_families=("artifacts",))

    target_paths = {record.target for record in result.records}
    assert "core/control_plane/manifests/pack_settings.json" in target_paths
    assert "core/control_plane/registries/pack_registry.json" in target_paths
    assert "core/control_plane/registries/schema_catalog.json" in target_paths
    assert "core/control_plane/indexes/foundations/foundation_index.json" in target_paths
    assert "plan/.wt/manifests/pack_runtime_manifest.json" in target_paths
    assert all(
        not target_path.startswith("core/control_plane/examples/") for target_path in target_paths
    )
    assert result.passed is True

def test_validate_all_reuses_reference_index_build_across_workflow_semantics(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = _service_with_targets(
        {
            "step.plan.document_semantics": (
                "core/workflows/modules/code_validation.md",
                "core/workflows/modules/code_review.md",
            )
        }
    )
    reference_build_count = 0
    original_build_document = ReferenceIndexSyncService.build_document

    def wrapped_build_document(
        self: ReferenceIndexSyncService,
    ) -> dict[str, object]:
        nonlocal reference_build_count
        reference_build_count += 1
        return original_build_document(self)

    monkeypatch.setattr(
        ReferenceIndexSyncService,
        "build_document",
        wrapped_build_document,
    )

    result = service.run(included_families=("document_semantics",))

    assert result.passed is True
    assert reference_build_count == 1


def test_validate_all_reuses_validator_registry_materialization(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = _service()
    validator_registry_path = service._loader.load_pack_settings().get("validator_registry").path
    validator_registry_document_loads = 0
    original_load_validated_document = service._loader.load_validated_document

    def wrapped_load_validated_document(relative_path: str) -> dict[str, Any]:
        nonlocal validator_registry_document_loads
        if relative_path == validator_registry_path:
            validator_registry_document_loads += 1
        return original_load_validated_document(relative_path)

    monkeypatch.setattr(
        service._loader,
        "load_validated_document",
        wrapped_load_validated_document,
    )

    result = service.run()

    assert result.passed is True
    assert validator_registry_document_loads == 1


def test_validate_all_reuses_acceptance_reconciliation_snapshots(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = _service()
    counts: Counter[str] = Counter()

    for name in (
        "load_traceability_index",
        "load_acceptance_contracts",
        "load_validation_evidence_artifacts",
        "load_validator_registry",
    ):
        original = getattr(service._loader, name)

        def make_wrapper(
            method_name: str,
            method: Callable[..., object],
        ) -> Callable[..., object]:
            def wrapped(*args: object, **kwargs: object) -> object:
                counts[method_name] += 1
                return method(*args, **kwargs)

            return wrapped

        monkeypatch.setattr(service._loader, name, make_wrapper(name, original))

    result = service.run(included_families=("acceptance",))

    assert result.passed is True
    assert counts == {
        "load_traceability_index": 1,
        "load_acceptance_contracts": 1,
        "load_validation_evidence_artifacts": 1,
        "load_validator_registry": 1,
    }


def test_validate_all_reports_missing_repo_local_acceptance_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    contract_path = (
        repo_root
        / "core/control_plane/contracts/acceptance/"
        "governed_acceptance_example_acceptance.json"
    )
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    contract["entries"][0]["validation_targets"].append(
        "plan/initiatives/missing/.wt/tasks/missing/task.json"
    )
    contract_path.write_text(f"{json.dumps(contract, indent=2)}\n", encoding="utf-8")

    service = _service(repo_root)
    monkeypatch.setattr(
        service._acceptance,
        "acceptance_trace_ids",
        lambda: ("trace.governed_acceptance_example",),
    )
    result = service.run(included_families=("acceptance",))

    assert result.passed is False
    assert result.failed_count == 1
    assert result.records[0].family == "acceptance"
    assert any(
        issue.code == "acceptance_validation_target_missing"
        for issue in result.records[0].result.issues
    )
