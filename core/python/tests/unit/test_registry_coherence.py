"""Structural coherence tests for cross-registry references.

Validates that every identifier referenced across the route index,
workflow index, overlay registry, and merge policy registry actually
exists in the target registry.  Catches typos, stale references, and
silent no-ops before they become routing bugs.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.query.trusted_indexes import (
    load_trusted_route_index,
    load_trusted_workflow_index,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(scope="module")
def loader() -> ControlPlaneLoader:
    return ControlPlaneLoader(REPO_ROOT)


# ---------------------------------------------------------------------------
# Materialized index sets — computed once per module
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def route_task_types(loader: ControlPlaneLoader) -> set[str]:
    return {entry.task_type for entry in load_trusted_route_index(loader).entries}


@pytest.fixture(scope="module")
def route_ids(loader: ControlPlaneLoader) -> set[str]:
    return {entry.route_id for entry in load_trusted_route_index(loader).entries}


@pytest.fixture(scope="module")
def workflow_ids(loader: ControlPlaneLoader) -> set[str]:
    return {entry.workflow_id for entry in load_trusted_workflow_index(loader).entries}


@pytest.fixture(scope="module")
def overlay_ids(loader: ControlPlaneLoader) -> set[str]:
    return {entry.overlay_id for entry in loader.load_route_overlay_registry().entries}


# ===================================================================
# Route index → workflow index
# ===================================================================


class TestRouteIndexReferencesWorkflows:
    """Every required_workflow_id in the route index must exist in
    the workflow index."""

    def test_all_route_workflow_ids_exist(
        self,
        loader: ControlPlaneLoader,
        workflow_ids: set[str],
    ) -> None:
        route_index = load_trusted_route_index(loader)
        missing: list[tuple[str, str]] = []
        for entry in route_index.entries:
            for wid in entry.required_workflow_ids:
                if wid not in workflow_ids:
                    missing.append((entry.route_id, wid))

        assert not missing, (
            "Route index references workflow IDs that do not exist in the "
            "workflow index:\n"
            + "\n".join(f"  {route_id} → {wid}" for route_id, wid in missing)
        )

    def test_all_route_workflow_paths_are_nonempty(
        self,
        loader: ControlPlaneLoader,
    ) -> None:
        route_index = load_trusted_route_index(loader)
        empty: list[str] = [
            entry.route_id
            for entry in route_index.entries
            if not entry.required_workflow_paths
        ]
        assert not empty, f"Routes with empty workflow paths: {empty}"

    def test_route_ids_match_convention(
        self,
        loader: ControlPlaneLoader,
    ) -> None:
        """Route IDs should follow the route.<snake_case> convention."""
        route_index = load_trusted_route_index(loader)
        bad: list[str] = [
            entry.route_id
            for entry in route_index.entries
            if not entry.route_id.startswith("route.")
        ]
        assert not bad, f"Route IDs not following route.* convention: {bad}"


# ===================================================================
# Overlay registry → route index + workflow index + self-references
# ===================================================================


class TestOverlayRegistryReferences:
    """Overlay compatible_task_types, attached_route_task_types,
    attached_workflow_ids, and suppresses_intent_ids must all
    reference real entries."""

    def test_overlay_compatible_task_types_exist_in_route_index(
        self,
        loader: ControlPlaneLoader,
        route_task_types: set[str],
    ) -> None:
        registry = loader.load_route_overlay_registry()
        missing: list[tuple[str, str]] = []
        for overlay in registry.entries:
            for task_type in overlay.compatible_task_types:
                if task_type not in route_task_types:
                    missing.append((overlay.overlay_id, task_type))

        assert not missing, (
            "Overlay compatible_task_types reference unknown task types:\n"
            + "\n".join(f"  {oid} → {tt}" for oid, tt in missing)
        )

    def test_overlay_attached_route_task_types_exist_in_route_index(
        self,
        loader: ControlPlaneLoader,
        route_task_types: set[str],
    ) -> None:
        registry = loader.load_route_overlay_registry()
        missing: list[tuple[str, str]] = []
        for overlay in registry.entries:
            for task_type in overlay.attached_route_task_types:
                if task_type not in route_task_types:
                    missing.append((overlay.overlay_id, task_type))

        assert not missing, (
            "Overlay attached_route_task_types reference unknown task types:\n"
            + "\n".join(f"  {oid} → {tt}" for oid, tt in missing)
        )

    def test_overlay_attached_workflow_ids_exist_in_workflow_index(
        self,
        loader: ControlPlaneLoader,
        workflow_ids: set[str],
    ) -> None:
        registry = loader.load_route_overlay_registry()
        missing: list[tuple[str, str]] = []
        for overlay in registry.entries:
            for wid in overlay.attached_workflow_ids:
                if wid not in workflow_ids:
                    missing.append((overlay.overlay_id, wid))

        assert not missing, (
            "Overlay attached_workflow_ids reference unknown workflow IDs:\n"
            + "\n".join(f"  {oid} → {wid}" for oid, wid in missing)
        )

    def test_overlay_suppresses_intent_ids_reference_existing_overlays(
        self,
        loader: ControlPlaneLoader,
        overlay_ids: set[str],
    ) -> None:
        registry = loader.load_route_overlay_registry()
        missing: list[tuple[str, str]] = []
        for overlay in registry.entries:
            for suppressed_id in overlay.suppresses_intent_ids:
                if suppressed_id not in overlay_ids:
                    missing.append((overlay.overlay_id, suppressed_id))

        assert not missing, (
            "Overlay suppresses_intent_ids reference unknown overlay IDs:\n"
            + "\n".join(f"  {oid} → {sid}" for oid, sid in missing)
        )

    def test_overlay_excluded_task_types_exist_in_route_index(
        self,
        loader: ControlPlaneLoader,
        route_task_types: set[str],
    ) -> None:
        registry = loader.load_route_overlay_registry()
        missing: list[tuple[str, str]] = []
        for overlay in registry.entries:
            for task_type in overlay.excluded_task_types:
                if task_type not in route_task_types:
                    missing.append((overlay.overlay_id, task_type))

        assert not missing, (
            "Overlay excluded_task_types reference unknown task types:\n"
            + "\n".join(f"  {oid} → {tt}" for oid, tt in missing)
        )


# ===================================================================
# Merge policy registry → route index
# ===================================================================


class TestMergePolicyRegistryReferences:
    """Every task type referenced in merge policies must exist in
    the route index."""

    def test_merge_policy_suppress_task_types_exist(
        self,
        loader: ControlPlaneLoader,
        route_task_types: set[str],
    ) -> None:
        registry = loader.load_route_merge_policy_registry()
        missing: list[tuple[str, str]] = []
        for policy in registry.entries:
            for task_type in policy.suppress_task_types:
                if task_type not in route_task_types:
                    missing.append((policy.rule_id, task_type))

        assert not missing, (
            "Merge policy suppress_task_types reference unknown task types:\n"
            + "\n".join(f"  {rid} → {tt}" for rid, tt in missing)
        )

    def test_merge_policy_when_all_task_types_exist(
        self,
        loader: ControlPlaneLoader,
        route_task_types: set[str],
    ) -> None:
        registry = loader.load_route_merge_policy_registry()
        missing: list[tuple[str, str]] = []
        for policy in registry.entries:
            for task_type in policy.when_all_task_types_present:
                if task_type not in route_task_types:
                    missing.append((policy.rule_id, task_type))

        assert not missing, (
            "Merge policy when_all_task_types_present reference unknown task types:\n"
            + "\n".join(f"  {rid} → {tt}" for rid, tt in missing)
        )

    def test_merge_policy_when_any_task_types_exist(
        self,
        loader: ControlPlaneLoader,
        route_task_types: set[str],
    ) -> None:
        registry = loader.load_route_merge_policy_registry()
        missing: list[tuple[str, str]] = []
        for policy in registry.entries:
            for task_type in policy.when_any_task_types_present:
                if task_type not in route_task_types:
                    missing.append((policy.rule_id, task_type))

        assert not missing, (
            "Merge policy when_any_task_types_present reference unknown task types:\n"
            + "\n".join(f"  {rid} → {tt}" for rid, tt in missing)
        )


# ===================================================================
# Workflow index self-consistency
# ===================================================================


class TestWorkflowIndexConsistency:
    """Workflow index entries should be internally consistent."""

    def test_workflow_ids_follow_convention(
        self,
        loader: ControlPlaneLoader,
    ) -> None:
        workflow_index = load_trusted_workflow_index(loader)
        bad: list[str] = [
            entry.workflow_id
            for entry in workflow_index.entries
            if not entry.workflow_id.startswith("workflow.")
        ]
        assert not bad, f"Workflow IDs not following workflow.* convention: {bad}"

    def test_companion_workflow_ids_exist(
        self,
        loader: ControlPlaneLoader,
        workflow_ids: set[str],
    ) -> None:
        workflow_index = load_trusted_workflow_index(loader)
        missing: list[tuple[str, str]] = []
        for entry in workflow_index.entries:
            for companion_id in entry.companion_workflow_ids:
                if companion_id not in workflow_ids:
                    missing.append((entry.workflow_id, companion_id))

        assert not missing, (
            "Workflow companion_workflow_ids reference unknown workflow IDs:\n"
            + "\n".join(f"  {wid} → {cid}" for wid, cid in missing)
        )

    def test_no_duplicate_route_ids(
        self,
        loader: ControlPlaneLoader,
    ) -> None:
        route_index = load_trusted_route_index(loader)
        seen: dict[str, str] = {}
        duplicates: list[str] = []
        for entry in route_index.entries:
            if entry.route_id in seen:
                duplicates.append(
                    f"{entry.route_id} (task types: {seen[entry.route_id]!r}, {entry.task_type!r})"
                )
            seen[entry.route_id] = entry.task_type
        assert not duplicates, f"Duplicate route IDs: {duplicates}"

    def test_no_duplicate_task_types(
        self,
        loader: ControlPlaneLoader,
    ) -> None:
        route_index = load_trusted_route_index(loader)
        seen: dict[str, str] = {}
        duplicates: list[str] = []
        for entry in route_index.entries:
            if entry.task_type in seen:
                duplicates.append(
                    f"{entry.task_type} (route IDs: {seen[entry.task_type]!r}, {entry.route_id!r})"
                )
            seen[entry.task_type] = entry.route_id
        assert not duplicates, f"Duplicate task types: {duplicates}"

    def test_no_duplicate_workflow_ids(
        self,
        loader: ControlPlaneLoader,
    ) -> None:
        workflow_index = load_trusted_workflow_index(loader)
        seen: set[str] = set()
        duplicates: list[str] = []
        for entry in workflow_index.entries:
            if entry.workflow_id in seen:
                duplicates.append(entry.workflow_id)
            seen.add(entry.workflow_id)
        assert not duplicates, f"Duplicate workflow IDs: {duplicates}"
