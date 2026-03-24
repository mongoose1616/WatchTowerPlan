from __future__ import annotations

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation.context import PackValidationContext
from watchtower_core.validation.pack_targets import (
    artifact_targets,
    document_semantics_targets,
    front_matter_targets,
)


def _plan_validation_context() -> PackValidationContext:
    loader = ControlPlaneLoader(active_pack_settings_path="plan/.wt/manifests/pack_settings.json")
    return PackValidationContext.from_loader(
        loader,
        pack_settings_path="plan/.wt/manifests/pack_settings.json",
    )


def test_front_matter_targets_include_governed_markdown_docs() -> None:
    targets = front_matter_targets(_plan_validation_context())

    assert "core/docs/references/commonmark_reference.md" in targets
    assert "core/docs/foundations/product_direction.md" in targets
    assert "core/docs/standards/documentation/workflow_md_standard.md" in targets
    assert "core/workflows/modules/code_validation.md" not in targets
    assert "core/docs/commands/core_python/watchtower_core_pack_export.md" not in targets


def test_document_semantics_targets_include_command_docs() -> None:
    targets = document_semantics_targets(_plan_validation_context())

    assert "core/docs/commands/core_python/watchtower_core_pack_export.md" in targets
    assert "core/docs/commands/core_python/watchtower_core_validate_portability.md" in targets


def test_artifact_targets_exclude_schema_definitions_and_keep_artifacts() -> None:
    targets = artifact_targets(_plan_validation_context())

    assert "plan/.wt/work_items/pack_work_item_note_stage1_bootstrap.json" in targets
    assert "core/control_plane/schemas/interfaces/packs/benchmark_report.schema.json" not in targets
    assert (
        "core/control_plane/schemas/interfaces/packs/pack_work_item_note.schema.json"
        not in targets
    )
    assert (
        "core/control_plane/schemas/interfaces/packs/extraction_output_envelope.schema.json"
        not in targets
    )
