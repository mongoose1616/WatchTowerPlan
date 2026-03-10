"""Deterministic rebuild helpers for the route index."""

from __future__ import annotations

import json
import re
from pathlib import Path

from watchtower_core.adapters import parse_markdown_table
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root

ROUTING_TABLE_DOCUMENT_PATH = "workflows/ROUTING_TABLE.md"
ROUTE_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/routes/route_index.v1.json"
_ROUTE_TABLE_HEADER = "| Task Type | Trigger Keywords (Examples) | Required Workflows |"


def _route_id(task_type: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", task_type.casefold()).strip("_")
    return f"route.{slug}"


def _workflow_path(path: str) -> str:
    candidate = path.strip().strip("`")
    if not candidate.startswith("modules/"):
        raise ValueError(f"Route index found unexpected workflow path entry: {path}")
    return f"workflows/{candidate}"


def _workflow_id(workflow_path: str) -> str:
    return f"workflow.{Path(workflow_path).stem}"


def _extract_route_table(markdown: str) -> str:
    """Return only the routed task table from the routing document."""
    table_lines: list[str] = []
    collecting = False

    for line in markdown.splitlines():
        stripped = line.strip()
        if not collecting:
            if stripped == _ROUTE_TABLE_HEADER:
                collecting = True
                table_lines.append(stripped)
            continue
        if not stripped or not stripped.startswith("|"):
            break
        table_lines.append(stripped)

    if not table_lines:
        raise ValueError("Routing table document is missing the routed task table.")
    return "\n".join(table_lines)


class RouteIndexSyncService:
    """Build and write the route index from the routing table."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> RouteIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def build_document(self) -> dict[str, object]:
        routing_markdown = (self._repo_root / ROUTING_TABLE_DOCUMENT_PATH).read_text(
            encoding="utf-8"
        )
        rows = parse_markdown_table(_extract_route_table(routing_markdown))
        entries: list[dict[str, object]] = []

        for row in rows:
            task_type = row["Task Type"].strip()
            trigger_keywords = tuple(
                keyword.strip()
                for keyword in row["Trigger Keywords (Examples)"].split(",")
                if keyword.strip()
            )
            required_workflow_paths = tuple(
                _workflow_path(item)
                for item in row["Required Workflows"].split(",")
                if item.strip()
            )
            required_workflow_ids = tuple(
                _workflow_id(path) for path in required_workflow_paths
            )

            if not trigger_keywords:
                raise ValueError(f"Route row is missing trigger keywords: {task_type}")
            if not required_workflow_paths:
                raise ValueError(f"Route row is missing required workflows: {task_type}")

            for workflow_path in required_workflow_paths:
                if not (self._repo_root / workflow_path).exists():
                    raise ValueError(
                        f"Route row points to a missing workflow module: {task_type} -> "
                        f"{workflow_path}"
                    )

            entries.append(
                {
                    "route_id": _route_id(task_type),
                    "task_type": task_type,
                    "trigger_keywords": list(trigger_keywords),
                    "required_workflow_ids": list(required_workflow_ids),
                    "required_workflow_paths": list(required_workflow_paths),
                }
            )

        document: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:route-index:v1",
            "id": "index.routes",
            "title": "Route Index",
            "status": "active",
            "entries": entries,
        }
        self._loader.schema_store.validate_instance(document)
        return document

    def write_document(self, document: dict[str, object], destination: Path | None = None) -> Path:
        """Write the generated route index to disk."""
        target = destination or (self._repo_root / ROUTE_INDEX_ARTIFACT_PATH)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target
