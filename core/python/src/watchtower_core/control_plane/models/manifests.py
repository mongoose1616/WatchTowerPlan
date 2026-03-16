"""Typed models for runtime-boundary manifest artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class PackRuntimeWorkspaceRoots:
    """Declared logical workspace roots for one pack runtime."""

    repo_root: str
    control_plane: str
    python_workspace: str

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PackRuntimeWorkspaceRoots:
        return cls(
            repo_root=document["repo_root"],
            control_plane=document["control_plane"],
            python_workspace=document["python_workspace"],
        )


@dataclass(frozen=True, slots=True)
class PackRuntimeGovernedRoots:
    """Declared governed artifact roots for one pack runtime."""

    manifest_root: str
    schema_catalog: str
    registry_root: str
    contract_root: str
    index_root: str
    ledger_root: str

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PackRuntimeGovernedRoots:
        return cls(
            manifest_root=document["manifest_root"],
            schema_catalog=document["schema_catalog"],
            registry_root=document["registry_root"],
            contract_root=document["contract_root"],
            index_root=document["index_root"],
            ledger_root=document["ledger_root"],
        )


@dataclass(frozen=True, slots=True)
class PackRuntimeManifest:
    """Typed pack-runtime manifest artifact."""

    schema_id: str
    manifest_id: str
    title: str
    status: str
    pack_id: str
    core_package: str
    workspace_roots: PackRuntimeWorkspaceRoots
    governed_roots: PackRuntimeGovernedRoots
    supported_artifact_families: tuple[str, ...]
    derived_index_surfaces: tuple[str, ...]
    extension_points: tuple[str, ...]
    human_companion_roots: tuple[str, ...] = ()
    related_paths: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PackRuntimeManifest:
        return cls(
            schema_id=document["$schema"],
            manifest_id=document["id"],
            title=document["title"],
            status=document["status"],
            pack_id=document["pack_id"],
            core_package=document["core_package"],
            workspace_roots=PackRuntimeWorkspaceRoots.from_document(document["workspace_roots"]),
            governed_roots=PackRuntimeGovernedRoots.from_document(document["governed_roots"]),
            supported_artifact_families=tuple(document["supported_artifact_families"]),
            derived_index_surfaces=tuple(document["derived_index_surfaces"]),
            extension_points=tuple(document["extension_points"]),
            human_companion_roots=tuple(document.get("human_companion_roots", ())),
            related_paths=tuple(document.get("related_paths", ())),
            notes=document.get("notes"),
        )
