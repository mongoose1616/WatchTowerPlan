from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from watchtower_core.control_plane import ControlPlaneLoader, PackContext

REPO_ROOT = Path(__file__).resolve().parents[4]
CORE_PACK_SETTINGS_PATH = "core/control_plane/manifests/pack_settings.json"


def test_pack_context_loads_declared_pack_surfaces() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context(CORE_PACK_SETTINGS_PATH)

    assert isinstance(context, PackContext)
    assert context.pack_settings.pack_id == "pack.core_shared"
    assert context.workspace_roots.workspace_root == "core"
    assert context.schema_catalog.get(
        "urn:watchtower:schema:interfaces:packs:pack-settings:v1"
    ).canonical_relative_path == (
        "core/control_plane/schemas/interfaces/packs/pack_settings.schema.json"
    )
    assert (
        context.governance_surface_map.get("routing_table").path
        == "core/workflows/ROUTING_TABLE.md"
    )
    assert context.status_registry.get("accepted").entry_status == "active"
    assert context.actor_registry.get("actor.codex").actor_type == "agent"
    assert "rendered_surface_registry" in context.registries
    assert "validator_registry" in context.registries
    assert "validation_suite_registry" in context.registries
    assert (
        context.validation_suite_registry.get("suite.core.shared_validation_baseline")
        .get_step("step.core.artifacts")
        .step_kind
        == "artifact"
    )
    assert "coordination_index" not in context.indexes


def test_load_active_pack_context_activates_and_caches_effective_pack() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    first = loader.load_active_pack_context(CORE_PACK_SETTINGS_PATH)
    second = loader.load_active_pack_context()

    assert first is second
    assert loader.active_pack_settings_path == CORE_PACK_SETTINGS_PATH
    assert first.pack_settings_path == CORE_PACK_SETTINGS_PATH


def test_pack_context_exposes_loaded_surfaces_by_name() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context(CORE_PACK_SETTINGS_PATH)
    surface = context.get_surface("path_pattern_registry")

    assert surface is context.path_pattern_registry


def test_pack_context_loads_cleaned_shared_status_vocabulary() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context(CORE_PACK_SETTINGS_PATH)

    assert context.status_registry.get("blocked").allowed_families == ()
    assert context.status_registry.get("completed").entry_status == "active"
    assert context.status_registry.get("cancelled").entry_status == "active"


def test_pack_context_loads_required_surface_from_relocated_declared_path() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    base_settings = json.loads(
        (REPO_ROOT / CORE_PACK_SETTINGS_PATH).read_text(encoding="utf-8")
    )

    with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
        tmp_path = Path(tmp_dir)
        relocated_status_path = tmp_path / "status_registry.json"
        shutil.copy2(
            REPO_ROOT / "core/control_plane/registries/status_registry.json",
            relocated_status_path,
        )

        custom_settings = dict(base_settings)
        custom_settings["surfaces"] = [dict(entry) for entry in base_settings["surfaces"]]
        for entry in custom_settings["surfaces"]:
            if entry["surface_name"] == "status_registry":
                entry["path"] = relocated_status_path.relative_to(REPO_ROOT).as_posix()
                break
        custom_settings_path = tmp_path / "pack_settings.json"
        custom_settings_path.write_text(
            f"{json.dumps(custom_settings, indent=2)}\n",
            encoding="utf-8",
        )

        context = loader.load_pack_context(custom_settings_path.relative_to(REPO_ROOT).as_posix())

    assert context.status_registry.get("accepted").entry_status == "active"


def test_pack_context_skips_missing_rebuildable_derived_surface_until_built() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    base_settings = json.loads(
        (REPO_ROOT / CORE_PACK_SETTINGS_PATH).read_text(encoding="utf-8")
    )

    with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
        tmp_path = Path(tmp_dir)
        custom_settings = dict(base_settings)
        custom_settings["surfaces"] = [dict(entry) for entry in base_settings["surfaces"]]
        for entry in custom_settings["surfaces"]:
            if entry["surface_name"] == "route_index":
                entry["path"] = (
                    (tmp_path / "missing_route_index.json").relative_to(REPO_ROOT).as_posix()
                )
                break
        custom_settings_path = tmp_path / "pack_settings.json"
        custom_settings_path.write_text(
            f"{json.dumps(custom_settings, indent=2)}\n",
            encoding="utf-8",
        )

        context = loader.load_pack_context(custom_settings_path.relative_to(REPO_ROOT).as_posix())

    assert "route_index" not in context.indexes
    assert context.status_registry.get("accepted").entry_status == "active"
