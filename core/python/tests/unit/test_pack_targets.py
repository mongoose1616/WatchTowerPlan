from __future__ import annotations

from pathlib import Path

from tests.pack_fixture_support import (
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation.context import PackValidationContext
from watchtower_core.validation.pack_targets import (
    artifact_targets,
    document_semantics_targets,
    front_matter_targets,
)


def _pack_validation_context(
    tmp_path: Path,
) -> tuple[PackValidationContext, dict[str, str]]:
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
    pack_settings_path = str(surfaces["pack_settings_path"])
    loader = ControlPlaneLoader(
        repo_root=repo_root,
        active_pack_settings_path=pack_settings_path,
    )
    return (
        PackValidationContext.from_loader(
            loader,
            pack_settings_path=pack_settings_path,
        ),
        surfaces,
    )


def test_front_matter_targets_include_governed_markdown_docs(tmp_path: Path) -> None:
    context, _ = _pack_validation_context(tmp_path)
    targets = front_matter_targets(context)

    assert "core/docs/references/commonmark_reference.md" in targets
    assert "core/docs/foundations/product_direction.md" in targets
    assert "core/docs/standards/documentation/workflow_md_standard.md" in targets
    assert "core/workflows/modules/code_validation.md" not in targets
    assert "core/docs/commands/core_python/watchtower_core_pack_export.md" not in targets


def test_document_semantics_targets_include_command_docs(tmp_path: Path) -> None:
    context, _ = _pack_validation_context(tmp_path)
    targets = document_semantics_targets(context)

    assert "core/docs/commands/core_python/watchtower_core_pack_export.md" in targets
    assert "core/docs/commands/core_python/watchtower_core_validate_portability.md" in targets


def test_document_semantics_targets_include_workflow_modules_and_roles(tmp_path: Path) -> None:
    context, _ = _pack_validation_context(tmp_path)
    pack_module_path = context.loader.resolve_path(
        "packs/targets/workflows/modules/example_workflow.md"
    )
    pack_role_path = context.loader.resolve_path("packs/targets/workflows/roles/example_role.md")
    pack_module_path.parent.mkdir(parents=True, exist_ok=True)
    pack_role_path.parent.mkdir(parents=True, exist_ok=True)
    pack_module_path.write_text("# Example Workflow\n", encoding="utf-8")
    pack_role_path.write_text("# Example Role\n", encoding="utf-8")
    targets = document_semantics_targets(context)

    assert "core/workflows/modules/workflow_system_review.md" in targets
    assert "core/workflows/roles/workflow_steward.md" in targets
    assert "packs/targets/workflows/modules/example_workflow.md" in targets
    assert "packs/targets/workflows/roles/example_role.md" in targets
    assert "core/workflows/README.md" not in targets
    assert "plan/workflows/roles/README.md" not in targets


def test_markdown_targets_include_pack_owned_reference_docs(tmp_path: Path) -> None:
    context, _ = _pack_validation_context(tmp_path)
    relative_path = "packs/targets/docs/references/example_reference.md"
    target_path = context.loader.resolve_path(relative_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text("# Placeholder\n", encoding="utf-8")

    assert relative_path in front_matter_targets(context)
    assert relative_path in document_semantics_targets(context)


def test_artifact_targets_exclude_schema_definitions_and_keep_artifacts(
    tmp_path: Path,
) -> None:
    context, surfaces = _pack_validation_context(tmp_path)
    targets = artifact_targets(context)

    assert str(surfaces["artifact_relative_path"]) in targets
    assert "core/control_plane/schemas/artifacts/benchmark_record.schema.json" not in targets
    assert "core/control_plane/schemas/artifacts/benchmark_suite_registry.schema.json" not in targets
    assert (
        "core/control_plane/schemas/interfaces/packs/pack_work_item_note.schema.json"
        not in targets
    )
    assert (
        "core/control_plane/schemas/interfaces/packs/extraction_output_envelope.schema.json"
        not in targets
    )
