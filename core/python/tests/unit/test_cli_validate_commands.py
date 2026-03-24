from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

from tests.pack_fixture_support import (
    REPO_ROOT,
    materialize_externalized_fixture_python,
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_host.cli.main import main

REHOSTED_PACK_SLUG = "rehosted"
REHOSTED_PYTHON_DISTRIBUTION = "watchtower-rehosted-fixture"
REHOSTED_PYTHON_PACKAGE = "watchtower_rehosted_fixture"
REHOSTED_INTEGRATION_MODULE = "watchtower_rehosted_fixture.integration"


def _expected_cli_exit(payload: dict[str, object]) -> int:
    return 0 if bool(payload.get("passed")) else 1


def _materialize_unbootstrapped_rehosted_root_pack(repo_root: Path) -> dict[str, str]:
    surfaces = materialize_pack_validation_suite(
        repo_root / REHOSTED_PACK_SLUG,
        pack_id=f"pack.{REHOSTED_PACK_SLUG}",
        pack_slug=REHOSTED_PACK_SLUG,
        command_namespace=REHOSTED_PACK_SLUG,
        python_distribution=REHOSTED_PYTHON_DISTRIBUTION,
        python_package=REHOSTED_PYTHON_PACKAGE,
        integration_module=REHOSTED_INTEGRATION_MODULE,
        register_with_host_registry=False,
        register_with_core_python_workspace=False,
    )
    materialize_externalized_fixture_python(
        repo_root / REHOSTED_PACK_SLUG / "python",
        python_distribution=REHOSTED_PYTHON_DISTRIBUTION,
        python_package=REHOSTED_PYTHON_PACKAGE,
        source_package_root=(
            REPO_ROOT
            / "core"
            / "python"
            / "tests"
            / "fixtures"
            / "python"
                / "watchtower_oversight_fixture"
        ),
        description="Synthetic rehosted runtime package used to prove hosted-pack portability.",
    )
    return surfaces


def test_validate_front_matter_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "front-matter",
            "--path",
            "core/docs/standards/metadata/front_matter_standard.md",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate front-matter"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.documentation.standard_front_matter"


def test_validate_front_matter_reports_validation_failure(tmp_path: Path, capsys) -> None:
    document_path = tmp_path / "missing_front_matter.md"
    document_path.write_text("# Missing front matter\n", encoding="utf-8")

    result = main(
        [
            "validate",
            "front-matter",
            "--path",
            str(document_path),
            "--validator-id",
            "validator.documentation.standard_front_matter",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload["command"] == "watchtower-core validate front-matter"
    assert payload["status"] == "ok"
    assert payload["passed"] is False
    assert payload["issue_count"] == 1
    assert payload["issues"][0]["code"] == "front_matter_missing"


def test_validate_front_matter_can_record_evidence_to_temp_outputs(tmp_path: Path, capsys) -> None:
    evidence_output = tmp_path / "validation_evidence.json"
    traceability_output = tmp_path / "traceability_index.json"

    result = main(
        [
            "validate",
            "front-matter",
            "--path",
            "core/docs/standards/metadata/front_matter_standard.md",
            "--record-evidence",
            "--trace-id",
            "trace.governed_acceptance_example",
            "--subject-id",
            "std.metadata.front_matter",
            "--evidence-output",
            str(evidence_output),
            "--traceability-output",
            str(traceability_output),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["passed"] is True
    assert payload["evidence"]["trace_id"] == "trace.governed_acceptance_example"
    assert evidence_output.exists()
    assert traceability_output.exists()


def test_validate_document_semantics_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "document-semantics",
            "--path",
            "core/workflows/modules/code_validation.md",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate document-semantics"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.documentation.workflow_semantics"


def test_validate_document_semantics_auto_selects_command_validator(capsys) -> None:
    result = main(
        [
            "validate",
            "document-semantics",
            "--path",
            "core/docs/commands/core_python/watchtower_core_pack_export.md",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate document-semantics"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.documentation.command_semantics"


def test_validate_artifact_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "artifact",
            "--path",
            "core/control_plane/contracts/acceptance/governed_acceptance_example_acceptance.json",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate artifact"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.control_plane.acceptance_contract"


def test_validate_artifact_reports_parse_failure(tmp_path: Path, capsys) -> None:
    document_path = tmp_path / "invalid.json"
    document_path.write_text("{ invalid json", encoding="utf-8")

    result = main(
        [
            "validate",
            "artifact",
            "--path",
            str(document_path),
            "--validator-id",
            "validator.control_plane.acceptance_contract",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload["command"] == "watchtower-core validate artifact"
    assert payload["status"] == "ok"
    assert payload["passed"] is False
    assert payload["issue_count"] == 1
    assert payload["issues"][0]["code"] == "json_parse_invalid"


def test_validate_schema_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "schema",
            "--path",
            "core/control_plane/schemas/interfaces/packs/pack_settings.schema.json",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate schema"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.schema_definition.draft2020_12"


def test_validate_schema_reports_invalid_schema(
    tmp_path: Path,
    capsys,
    json_writer,
) -> None:
    schema_path = tmp_path / "invalid.schema.json"
    json_writer(
        schema_path,
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "urn:watchtower:schema:test:invalid-cli:v1",
            "type": 42,
        },
    )

    result = main(
        [
            "validate",
            "schema",
            "--path",
            str(schema_path),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload["command"] == "watchtower-core validate schema"
    assert payload["status"] == "ok"
    assert payload["passed"] is False
    assert payload["issue_count"] >= 1
    assert payload["issues"][0]["code"] == "schema_definition_validation_error"


def test_validate_schema_can_record_evidence_to_temp_outputs(tmp_path: Path, capsys) -> None:
    evidence_output = tmp_path / "validation_evidence.json"
    traceability_output = tmp_path / "traceability_index.json"

    result = main(
        [
            "validate",
            "schema",
            "--path",
            "core/control_plane/schemas/interfaces/packs/pack_settings.schema.json",
            "--record-evidence",
            "--trace-id",
            "trace.governed_acceptance_example",
            "--subject-id",
            "schema.pack_settings",
            "--evidence-output",
            str(evidence_output),
            "--traceability-output",
            str(traceability_output),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["passed"] is True
    assert payload["evidence"]["trace_id"] == "trace.governed_acceptance_example"
    assert evidence_output.exists()
    assert traceability_output.exists()


def test_validate_artifact_supports_external_schema_id_and_supplemental_schema_path(
    tmp_path: Path,
    capsys,
    json_writer,
) -> None:
    schema_path = tmp_path / "schemas" / "external_note.schema.json"
    artifact_path = tmp_path / "artifacts" / "external_note.json"
    schema_id = "urn:watchtower:schema:external:cli-pack-note:v1"
    json_writer(
        schema_path,
        {
            "$id": schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "CLI Pack Note",
            "description": "External pack note schema loaded through CLI options.",
            "type": "object",
            "properties": {"kind": {"const": "cli_pack_note"}},
            "required": ["kind"],
            "additionalProperties": False,
        },
    )
    json_writer(artifact_path, {"kind": "cli_pack_note"})

    result = main(
        [
            "validate",
            "artifact",
            "--path",
            str(artifact_path),
            "--schema-id",
            schema_id,
            "--supplemental-schema-path",
            str(schema_path),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate artifact"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == f"schema:{schema_id}"
    assert payload["schema_ids"] == [schema_id]


def test_validate_artifact_reports_invalid_supplemental_schema_path(
    tmp_path: Path,
    capsys,
    json_writer,
) -> None:
    artifact_path = tmp_path / "artifacts" / "external_note.json"
    missing_schema_path = tmp_path / "schemas" / "missing"
    json_writer(artifact_path, {"kind": "cli_pack_note"})

    result = main(
        [
            "validate",
            "artifact",
            "--path",
            str(artifact_path),
            "--schema-id",
            "urn:watchtower:schema:external:cli-pack-note:v1",
            "--supplemental-schema-path",
            str(missing_schema_path),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload["command"] == "watchtower-core validate artifact"
    assert payload["status"] == "error"
    assert "Supplemental schema path does not exist" in payload["message"]


def test_validate_artifact_can_record_evidence_to_temp_outputs(tmp_path: Path, capsys) -> None:
    evidence_output = tmp_path / "validation_evidence.json"
    traceability_output = tmp_path / "traceability_index.json"

    result = main(
        [
            "validate",
            "artifact",
            "--path",
            "core/control_plane/contracts/acceptance/governed_acceptance_example_acceptance.json",
            "--record-evidence",
            "--trace-id",
            "trace.governed_acceptance_example",
            "--acceptance-id",
            "ac.governed_acceptance_example.001",
            "--evidence-output",
            str(evidence_output),
            "--traceability-output",
            str(traceability_output),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["passed"] is True
    assert payload["evidence"]["trace_id"] == "trace.governed_acceptance_example"
    assert evidence_output.exists()
    assert traceability_output.exists()


def test_validate_acceptance_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "acceptance",
            "--trace-id",
            "trace.governed_acceptance_example",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate acceptance"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.trace.acceptance_reconciliation"


def test_validate_all_supports_json_output_when_acceptance_is_skipped(capsys) -> None:
    result = main(["validate", "all", "--skip-acceptance", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == _expected_cli_exit(payload)
    assert payload["command"] == "watchtower-core validate all"
    assert payload["status"] == "ok"
    assert payload["included_families"] == [
        "pack_contract",
        "front_matter",
        "document_semantics",
        "artifacts",
    ]
    assert any(summary["family"] == "pack_contract" for summary in payload["family_summaries"])
    assert any(summary["family"] == "front_matter" for summary in payload["family_summaries"])
    assert any(summary["family"] == "document_semantics" for summary in payload["family_summaries"])
    assert any(summary["family"] == "artifacts" for summary in payload["family_summaries"])


def test_validate_all_supports_json_output(capsys) -> None:
    result = main(["validate", "all", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == _expected_cli_exit(payload)
    assert payload["command"] == "watchtower-core validate all"
    assert payload["status"] == "ok"


def test_validate_all_reports_unbootstrapped_root_pack_without_crashing(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    _materialize_unbootstrapped_rehosted_root_pack(repo_root)
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "validate",
            "all",
            "--skip-front-matter",
            "--skip-document-semantics",
            "--skip-artifacts",
            "--skip-acceptance",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload["command"] == "watchtower-core validate all"
    assert payload["status"] == "ok"
    assert payload["passed"] is False
    assert payload["included_families"] == ["pack_contract"]
    assert payload["failed_count"] == 1
    assert payload["results"][0]["family"] == "pack_contract"
    issue_codes = {issue["code"] for issue in payload["results"][0]["issues"]}
    assert "pack_workspace_dependency_missing" in issue_codes
    assert "pack_workspace_source_missing" in issue_codes
    assert issue_codes & {
        "pack_registry_entry_missing",
        "pack_contract_python_distribution_mismatch",
        "pack_contract_python_package_mismatch",
    }


def test_validate_portability_supports_json_output_for_clean_root(
    tmp_path: Path,
    capsys,
) -> None:
    (tmp_path / "README.md").write_text("# Clean export\n", encoding="utf-8")

    result = main(
        [
            "validate",
            "portability",
            "--root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate portability"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.portability.repository_export"
    assert payload["included_pack_slugs"] == []
    assert payload["scope"] == "repository_bundle"


def test_validate_portability_supports_pack_only_scope_for_clean_bundle(
    tmp_path: Path,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    recipient_root = repo_root / "packs" / "recipient"
    materialize_pack_validation_suite(
        recipient_root,
        pack_slug="recipient",
        registry_mode="replace_default",
        default_repo_pack=True,
    )

    bundle_root = tmp_path / "pack_bundle"
    copytree(recipient_root, bundle_root / "packs" / "recipient")

    result = main(
        [
            "validate",
            "portability",
            "--root",
            str(bundle_root),
            "--include-pack",
            "recipient",
            "--pack-only",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate portability"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["included_pack_slugs"] == ["recipient"]
    assert payload["scope"] == "pack_bundle"


def test_validate_portability_reports_release_exclusions(
    tmp_path: Path,
    capsys,
) -> None:
    (tmp_path / "core/control_plane/records/releases").mkdir(parents=True)
    (tmp_path / "core/control_plane/records/README.md").write_text(
        "# Records\n",
        encoding="utf-8",
    )
    (tmp_path / "core/control_plane/records/releases/example.json").write_text(
        "{}\n",
        encoding="utf-8",
    )
    (tmp_path / "core/control_plane/contracts/acceptance").mkdir(parents=True)
    (
        tmp_path / "core/control_plane/contracts/acceptance/example_acceptance.json"
    ).write_text(
        "{}\n",
        encoding="utf-8",
    )
    (tmp_path / "core/control_plane/indexes/traceability").mkdir(parents=True)
    (
        tmp_path / "core/control_plane/indexes/traceability/traceability_index.json"
    ).write_text(
        json.dumps(
            {
                "$schema": "urn:watchtower:schema:artifacts:indexes:traceability-index:v1",
                "id": "index.traceability",
                "title": "Traceability Index",
                "status": "active",
                "entries": [
                    {
                        "trace_id": "trace.acceptance_example",
                        "title": "Acceptance Example",
                        "summary": "Internal example traceability lineage.",
                        "status": "active",
                        "initiative_status": "completed",
                        "updated_at": "2026-03-25T03:00:00Z",
                        "closed_at": "2026-03-25T03:00:00Z",
                        "closure_reason": "Internal example only.",
                        "acceptance_ids": ["ac.acceptance_example.001"],
                        "acceptance_contract_ids": ["contract.acceptance.acceptance_example"],
                        "evidence_ids": ["evidence.acceptance_example.validation_baseline"],
                    }
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (tmp_path / "core/control_plane/registries").mkdir(parents=True)
    (tmp_path / "core/control_plane/registries/pack_registry.json").write_text(
        json.dumps(
            {
                "packs": [
                    {
                        "pack_slug": "plan",
                        "pack_settings_path": "plan/.wt/manifests/pack_settings.json",
                        "python_distribution": "watchtower-plan",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "core/python").mkdir(parents=True)
    (tmp_path / "core/python/pyproject.toml").write_text(
        "\n".join(
            (
                "[project]",
                'name = "watchtower-core"',
                "[project.optional-dependencies]",
                'dev = ["watchtower-plan"]',
                "[tool.uv.sources]",
                'watchtower-plan = { path = "../../plan/python", editable = true }',
            )
        )
        + "\n",
        encoding="utf-8",
    )
    (tmp_path / "core/python/tests/unit").mkdir(parents=True)
    (tmp_path / "core/python/tests/unit/test_example.py").write_text("", encoding="utf-8")
    (tmp_path / ".venv/bin").mkdir(parents=True)
    (tmp_path / "plan/.wt/runtime/telemetry").mkdir(parents=True)
    (tmp_path / "plan/python/tests/integration").mkdir(parents=True)
    (tmp_path / "plan/python/tests/integration/test_example.py").write_text(
        "",
        encoding="utf-8",
    )
    (tmp_path / "plan/python/src/watchtower_plan/testing").mkdir(parents=True)
    (tmp_path / "plan/python/src/watchtower_plan/testing/helper.py").write_text(
        "",
        encoding="utf-8",
    )
    (tmp_path / "plan/projects/watchtower/.wt").mkdir(parents=True)
    (tmp_path / "plan/projects/watchtower/.wt/project_repository_map.json").write_text(
        "{}\n",
        encoding="utf-8",
    )
    (tmp_path / "plan/docs/references").mkdir(parents=True)
    (
        tmp_path / "plan/docs/references/donor_assessment_closeout_reference.md"
    ).write_text(
        "# Donor Assessment\n",
        encoding="utf-8",
    )
    (tmp_path / "plan/README.md").write_text(
        "Local donor path: /home/j/WatchTowerPlan\n",
        encoding="utf-8",
    )

    result = main(
        [
            "validate",
            "portability",
            "--root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    issue_codes = {issue["code"] for issue in payload["issues"]}
    assert result == 1
    assert payload["command"] == "watchtower-core validate portability"
    assert payload["status"] == "ok"
    assert payload["passed"] is False
    assert payload["scope"] == "repository_bundle"
    assert issue_codes >= {
        "acceptance_contract_present",
        "absolute_donor_path_present",
        "developer_residue_present",
        "donor_project_map_present",
        "internal_assessment_document_present",
        "omitted_pack_registry_entry",
        "omitted_pack_root_present",
        "pack_runtime_state_present",
        "pack_testing_module_present",
        "retained_history_present",
        "test_surface_present",
        "traceability_acceptance_lineage_present",
        "workspace_pack_dependency_present",
        "workspace_pack_source_present",
    }


def test_validate_portability_pack_only_reports_pack_bundle_exclusions(
    tmp_path: Path,
    capsys,
) -> None:
    bundle_root = tmp_path / "pack_bundle"
    (bundle_root / "core/control_plane/records/releases").mkdir(parents=True)
    (bundle_root / "core/control_plane/records/releases/example.json").write_text(
        "{}\n",
        encoding="utf-8",
    )
    (bundle_root / "packs/recipient/.wt/manifests").mkdir(parents=True)
    (bundle_root / "packs/recipient/.wt/manifests/pack_runtime_manifest.json").write_text(
        json.dumps(
            {
                "pack_slug": "recipient",
                "owned_roots": {
                    "workspace_root": "packs/recipient",
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (bundle_root / "packs/recipient/.wt/runtime/telemetry").mkdir(parents=True)
    (bundle_root / "packs/recipient/python/tests/unit").mkdir(parents=True)
    (bundle_root / "packs/recipient/python/tests/unit/test_example.py").write_text(
        "",
        encoding="utf-8",
    )
    (bundle_root / "packs/recipient/python/src/watchtower_recipient/testing").mkdir(
        parents=True,
        exist_ok=True,
    )
    (
        bundle_root / "packs/recipient/python/src/watchtower_recipient/testing/helper.py"
    ).write_text(
        "",
        encoding="utf-8",
    )
    (bundle_root / "packs/recipient/projects/example/.wt").mkdir(parents=True)
    (
        bundle_root / "packs/recipient/projects/example/.wt/project_repository_map.json"
    ).write_text(
        "{}\n",
        encoding="utf-8",
    )
    (bundle_root / "packs/recipient/docs/references").mkdir(parents=True)
    (
        bundle_root / "packs/recipient/docs/references/recipient_assessment_closeout_reference.md"
    ).write_text(
        "# Internal Assessment\n",
        encoding="utf-8",
    )
    (bundle_root / "README.md").write_text(
        "Local donor path: /home/j/WatchTowerPlan\n",
        encoding="utf-8",
    )

    result = main(
        [
            "validate",
            "portability",
            "--root",
            str(bundle_root),
            "--include-pack",
            "recipient",
            "--pack-only",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    issue_codes = {issue["code"] for issue in payload["issues"]}
    assert result == 1
    assert payload["command"] == "watchtower-core validate portability"
    assert payload["status"] == "ok"
    assert payload["passed"] is False
    assert payload["scope"] == "pack_bundle"
    assert issue_codes >= {
        "absolute_donor_path_present",
        "donor_project_map_present",
        "internal_assessment_document_present",
        "pack_runtime_state_present",
        "pack_testing_module_present",
        "retained_history_present",
        "shared_core_surface_present",
        "test_surface_present",
    }


def test_validate_suite_supports_json_output(capsys) -> None:
    suite_id = ControlPlaneLoader(REPO_ROOT).load_pack_settings().default_validation_suite_id

    result = main(
        [
            "validate",
            "suite",
            "--suite-id",
            suite_id,
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == _expected_cli_exit(payload)
    assert payload["command"] == "watchtower-core validate suite"
    assert payload["status"] == "ok"
    assert payload["suite_id"] == suite_id
    assert isinstance(payload["passed"], bool)
    assert any(summary["step_kind"] == "front_matter" for summary in payload["step_summaries"])
    assert any(
        summary["step_kind"] == "document_semantics" for summary in payload["step_summaries"]
    )
    assert any(summary["step_kind"] == "artifact" for summary in payload["step_summaries"])


def test_validate_artifact_uses_pack_settings_path_to_select_pack_registry(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    monkeypatch.chdir(repo_root / "core" / "python")
    result = main(
        [
            "validate",
            "artifact",
            "--path",
            surfaces["artifact_relative_path"],
            "--pack-settings-path",
            surfaces["pack_settings_path"],
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate artifact"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == surfaces["validator_id"]
