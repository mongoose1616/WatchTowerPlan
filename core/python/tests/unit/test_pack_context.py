from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane import ControlPlaneLoader, PackContext

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_pack_context_loads_declared_step1_surfaces() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context()

    assert isinstance(context, PackContext)
    assert context.pack_settings.pack_id == "pack.watchtower_plan"
    assert context.schema_catalog.get(
        "urn:watchtower:schema:interfaces:packs:pack-settings:v1"
    ).canonical_relative_path == (
        "core/control_plane/schemas/interfaces/packs/pack_settings.schema.json"
    )
    assert context.governance_surface_map.get("routing_table").path == "workflows/ROUTING_TABLE.md"
    assert context.status_registry.get("accepted").entry_status == "active"
    assert context.actor_registry.get("actor.codex").actor_type == "agent"
    assert "validator_registry" in context.registries
    assert "route_index" in context.indexes


def test_pack_context_exposes_loaded_surfaces_by_name() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    context = loader.load_pack_context()
    surface = context.get_surface("path_pattern_registry")

    assert surface is context.path_pattern_registry
