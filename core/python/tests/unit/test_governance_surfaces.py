from __future__ import annotations

import json
import tempfile
from pathlib import Path

from watchtower_core.control_plane.governance_surfaces import GovernanceSurfaceResolver
from watchtower_core.control_plane.loader import ControlPlaneLoader

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_governance_surface_resolver_resolves_pack_declared_surface() -> None:
    resolver = GovernanceSurfaceResolver.from_loader(ControlPlaneLoader(REPO_ROOT))

    resolution = resolver.resolve("route_index")

    assert resolution.path == "core/control_plane/indexes/routes/route_index.json"
    assert resolution.authority == "derived"
    assert resolution.rebuildable is True
    assert resolution.declaration_sources == ("pack_settings",)


def test_governance_surface_resolver_resolves_governance_map_surface() -> None:
    resolver = GovernanceSurfaceResolver.from_loader(ControlPlaneLoader(REPO_ROOT))

    resolution = resolver.resolve("routing_table")

    assert resolution.path == "core/workflows/ROUTING_TABLE.md"
    assert resolution.authoritative is True
    assert resolution.rebuildable is False
    assert resolution.declaration_sources == ("governance_surface_map",)


def test_governance_surface_resolver_reports_declared_dependents() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    base_settings = json.loads(
        (REPO_ROOT / "core/control_plane/manifests/pack_settings.json").read_text(
            encoding="utf-8"
        )
    )

    with tempfile.TemporaryDirectory(dir=REPO_ROOT) as tmp_dir:
        tmp_path = Path(tmp_dir)
        custom_settings = dict(base_settings)
        custom_settings["surfaces"] = [dict(entry) for entry in base_settings["surfaces"]]
        custom_settings["surfaces"].extend(
            (
                {
                    "surface_name": "machine_summary",
                    "surface_kind": "registry",
                    "path": "core/control_plane/registries/validator_registry.json",
                    "authority": "authoritative",
                    "visibility": "hidden",
                },
                {
                    "surface_name": "summary_view",
                    "surface_kind": "index",
                    "path": "tmp/summary_view.md",
                    "authority": "derived",
                    "visibility": "user",
                    "rebuildable": True,
                    "source_surface": "machine_summary",
                },
                {
                    "surface_name": "summary_board",
                    "surface_kind": "index",
                    "path": "tmp/summary_board.json",
                    "authority": "derived",
                    "visibility": "mixed",
                    "rebuildable": True,
                    "depends_on": ["machine_summary"],
                    "builder": "watchtower_core.tests.summary_board",
                },
            )
        )
        custom_settings_path = tmp_path / "pack_settings.json"
        custom_settings_path.write_text(
            f"{json.dumps(custom_settings, indent=2)}\n",
            encoding="utf-8",
        )

        resolver = GovernanceSurfaceResolver.from_loader(
            loader,
            pack_settings_path=custom_settings_path.relative_to(REPO_ROOT).as_posix(),
        )

    resolution = resolver.resolve("machine_summary")

    assert resolution.path == "core/control_plane/registries/validator_registry.json"
    assert resolution.dependent_surface_names == ("summary_board", "summary_view")
