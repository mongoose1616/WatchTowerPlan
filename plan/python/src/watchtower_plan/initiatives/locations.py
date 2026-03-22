"""Location, loader, and artifact-path helpers for live initiative packages."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, TypeAlias, cast

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.pack_workspace import PackWorkspacePaths
from watchtower_core.control_plane.path_ids import PlanInitiativeLocation
from watchtower_plan.projects import ProjectWorkspaceService
from watchtower_plan.sync.coordination import CoordinationSyncService
from watchtower_plan.workspace.constants import PLAN_PACK_SETTINGS_PATH
from watchtower_plan.workspace.service import PlanWorkspaceService

from watchtower_plan.initiatives.models import InitiativeBootstrapParams

InitiativeLocation: TypeAlias = PlanInitiativeLocation


class InitiativeLocationManager:
    """Resolve initiative locations and provide shared filesystem helpers."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def pack_loader(self) -> ControlPlaneLoader:
        return self.fresh_loader(active_pack_settings_path=PLAN_PACK_SETTINGS_PATH)

    def fresh_loader(
        self,
        *,
        active_pack_settings_path: str | None = None,
    ) -> ControlPlaneLoader:
        return ControlPlaneLoader(
            workspace_config=self._loader.workspace_config,
            schema_store=self._loader.schema_store,
            artifact_source=self._loader.artifact_source,
            artifact_store=self._loader.artifact_store,
            active_pack_settings_path=active_pack_settings_path,
        )

    def workspace_paths(self) -> PackWorkspacePaths:
        return PackWorkspacePaths.from_loader(
            self.pack_loader(),
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )

    def packwide_location(
        self, params: InitiativeBootstrapParams
    ) -> InitiativeLocation:
        return self.workspace_paths().packwide_initiative_location(
            trace_id=params.trace_id,
            initiative_slug=params.initiative_slug,
        )

    def packwide_location_for_slug(self, initiative_slug: str) -> InitiativeLocation:
        return self.workspace_paths().packwide_initiative_location(
            initiative_slug=initiative_slug,
        )

    def project_scoped_location(
        self,
        project_slug: str,
        params: InitiativeBootstrapParams,
    ) -> InitiativeLocation:
        return self.workspace_paths().project_scoped_initiative_location(
            project_slug,
            trace_id=params.trace_id,
            initiative_slug=params.initiative_slug,
        )

    def project_scoped_location_for_slug(
        self,
        project_slug: str,
        initiative_slug: str,
    ) -> InitiativeLocation:
        return self.workspace_paths().project_scoped_initiative_location(
            project_slug,
            initiative_slug=initiative_slug,
        )

    def initiative_root(self, location: InitiativeLocation) -> Path:
        return self._loader.repo_root / location.initiative_root_relative

    def initiative_path(self, location: InitiativeLocation, suffix: str) -> str:
        return location.relative_path(suffix)

    def load_json(self, relative_path: str) -> dict[str, Any]:
        path = self._loader.repo_root / relative_path
        return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))

    def artifact_paths_for_location(
        self, location: InitiativeLocation
    ) -> tuple[str, ...]:
        initiative_root = self.initiative_root(location)
        relative_paths: list[str] = []
        for path in sorted(initiative_root.rglob("*.json")):
            relative_paths.append(str(path.relative_to(self._loader.repo_root)))
        return tuple(relative_paths)

    def artifact_documents(
        self,
        location: InitiativeLocation,
        suffix: str,
        pattern: str,
        *,
        task_pattern: bool = False,
    ) -> tuple[tuple[str, dict[str, Any]], ...]:
        root = self._loader.repo_root / self.initiative_path(location, suffix)
        if not root.exists():
            return ()
        if task_pattern:
            paths = sorted(root.glob("*/task.json"))
        else:
            paths = sorted(root.glob(pattern))
        return tuple(
            (
                str(path.relative_to(self._loader.repo_root)),
                json.loads(path.read_text(encoding="utf-8")),
            )
            for path in paths
        )

    def initiative_event_documents(
        self,
        location: InitiativeLocation,
    ) -> tuple[dict[str, Any], ...]:
        return tuple(
            document
            for _, document in self.artifact_documents(location, ".wt/events", "*.json")
        )

    def task_documents(
        self, location: InitiativeLocation
    ) -> tuple[dict[str, Any], ...]:
        return tuple(
            document
            for _, document in self.artifact_documents(
                location,
                ".wt/tasks",
                "task.json",
                task_pattern=True,
            )
        )

    def sha256_for_relative_path(self, relative_path: str) -> str:
        path = self._loader.repo_root / relative_path
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def initiative_identity_exists(self, initiative_id: str, trace_id: str) -> bool:
        workspace_paths = self.workspace_paths()
        roots = [self._loader.repo_root / workspace_paths.initiatives_root]
        projects_root = self._loader.repo_root / workspace_paths.projects_root
        if projects_root.exists():
            roots.extend(sorted(projects_root.glob("*/initiatives")))
        for root in roots:
            if not root.exists():
                continue
            for path in sorted(root.glob("*/.wt/initiative.json")):
                document = json.loads(path.read_text(encoding="utf-8"))
                if (
                    str(document.get("initiative_id")) == initiative_id
                    or str(document.get("trace_id")) == trace_id
                ):
                    return True
        return False

    def trace_id_exists(self, trace_id: str) -> bool:
        workspace_paths = self.workspace_paths()
        roots = [self._loader.repo_root / workspace_paths.initiatives_root]
        projects_root = self._loader.repo_root / workspace_paths.projects_root
        if projects_root.exists():
            roots.extend(sorted(projects_root.glob("*/initiatives")))
        for root in roots:
            if not root.exists():
                continue
            for path in sorted(root.glob("*/.wt/initiative.json")):
                document = json.loads(path.read_text(encoding="utf-8"))
                if str(document.get("trace_id")) == trace_id:
                    return True
        return False

    def has_execution_started(self, location: InitiativeLocation) -> bool:
        events_root = self.initiative_root(location) / ".wt" / "events"
        if not events_root.exists():
            return False
        for path in sorted(events_root.glob("*.json")):
            document = json.loads(path.read_text(encoding="utf-8"))
            if str(document.get("event_type")) == "execution_started":
                return True
        return False

    def sync_derived_surfaces(self, location: InitiativeLocation) -> None:
        fresh_loader = self.fresh_loader()
        if location.project_slug is not None:
            ProjectWorkspaceService(fresh_loader).sync(write=True)
        PlanWorkspaceService(fresh_loader).sync(write=True)
        CoordinationSyncService(fresh_loader).run(write=True)


__all__ = [
    "InitiativeLocation",
    "InitiativeLocationManager",
]
