from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest

from tests.integration.fixture_repo_support import (
    bootstrap_packwide_initiative,
    materialize_minimal_plan_pack,
)
from watchtower_core.control_plane.errors import ArtifactLoadError, SchemaResolutionError
from watchtower_core.control_plane.loader import (
    TRACEABILITY_INDEX_PATH,
    ControlPlaneLoader,
)
from watchtower_plan.plan_workspace import (
    PLAN_COORDINATION_INDEX_PATH as COORDINATION_INDEX_PATH,
    PLAN_INITIATIVE_INDEX_PATH as INITIATIVE_INDEX_PATH,
    PLAN_TASK_INDEX_PATH as TASK_INDEX_PATH,
)
from watchtower_plan.sync import AllSyncService, CoordinationSyncService
from watchtower_plan.sync.coordination_tracking import CoordinationTrackingSyncService
from watchtower_plan.sync.reference_index import ReferenceIndexSyncService
from watchtower_plan.sync.registry import (
    COORDINATION_SYNC_GROUP,
    SYNC_TARGET_SPECS,
    sync_target_specs_for_group,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
REFERENCE_RESOLUTION_SYNC_TARGETS = frozenset(
    {"reference-index", "foundation-index", "standard-index", "workflow-index"}
)


def _build_coordination_fixture_repo(repo_root: Path) -> Path:
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    materialize_minimal_plan_pack(repo_root, REPO_ROOT)
    bootstrap_packwide_initiative(
        repo_root,
        trace_id="trace.example_coordination_sync_dependency_fixture",
        title="Example Coordination Sync Dependency Fixture",
        summary="Seeds one live initiative so coordination dry-run sync exercises generated dependency artifacts.",
    )
    return repo_root


@pytest.fixture(scope="module")
def coordination_fixture_baseline(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return _build_coordination_fixture_repo(
        tmp_path_factory.mktemp("coordination_sync_baseline") / "repo"
    )


@pytest.fixture
def coordination_fixture_repo(tmp_path: Path, coordination_fixture_baseline: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(coordination_fixture_baseline, repo_root)
    return repo_root


@pytest.fixture(scope="module")
def all_sync_dry_run_result() -> object:
    loader = ControlPlaneLoader(REPO_ROOT)
    return AllSyncService(loader).run()


@pytest.fixture(scope="module")
def coordination_sync_dry_run_result() -> object:
    loader = ControlPlaneLoader(REPO_ROOT)
    return CoordinationSyncService(loader).run()


def _first_live_initiative_trace_id(repo_root: Path) -> str:
    for path in sorted((repo_root / "plan").rglob("initiative.json")):
        if "/.wt/" not in path.as_posix():
            continue
        document = json.loads(path.read_text(encoding="utf-8"))
        return str(document["trace_id"])
    raise AssertionError("Expected at least one live initiative package in the fixture repo.")


def test_all_sync_runs_in_dry_run_mode(all_sync_dry_run_result: object) -> None:
    result = all_sync_dry_run_result
    assert result.wrote is False
    assert tuple(record.target for record in result.records) == tuple(
        spec.target for spec in SYNC_TARGET_SPECS
    )


def test_all_sync_reuses_reference_index_build_for_dependent_targets(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = AllSyncService(loader)
    reference_specs = tuple(
        spec for spec in SYNC_TARGET_SPECS if spec.target in REFERENCE_RESOLUTION_SYNC_TARGETS
    )
    reference_build_count = 0
    original_build_document = ReferenceIndexSyncService.build_document

    def wrapped_build_document(
        self: ReferenceIndexSyncService,
    ) -> dict[str, object]:
        nonlocal reference_build_count
        reference_build_count += 1
        return original_build_document(self)

    monkeypatch.setattr(
        ReferenceIndexSyncService,
        "build_document",
        wrapped_build_document,
    )

    result = service.run_specs(reference_specs)

    assert result.wrote is False
    assert reference_build_count == 1


def test_sync_target_registry_is_unique() -> None:
    assert len({spec.target for spec in SYNC_TARGET_SPECS}) == len(SYNC_TARGET_SPECS)
    assert len({spec.relative_output_path for spec in SYNC_TARGET_SPECS}) == len(
        SYNC_TARGET_SPECS
    )


def test_coordination_sync_group_has_expected_targets_in_order() -> None:
    specs = sync_target_specs_for_group(COORDINATION_SYNC_GROUP)

    assert tuple(spec.target for spec in specs) == (
        "task-index",
        "traceability-index",
        "initiative-index",
        "coordination-index",
        "task-tracking",
        "initiative-tracking",
        "coordination-tracking",
    )


def test_coordination_sync_runs_in_dry_run_mode(
    coordination_sync_dry_run_result: object,
) -> None:
    result = coordination_sync_dry_run_result
    assert result.wrote is False
    assert tuple(record.target for record in result.records) == (
        "task-index",
        "traceability-index",
        "initiative-index",
        "coordination-index",
        "task-tracking",
        "initiative-tracking",
        "coordination-tracking",
    )


def test_coordination_sync_reuses_stable_rendered_sources(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = CoordinationSyncService(loader)
    source_read_counts: dict[str, int] = {
        TASK_INDEX_PATH: 0,
        TRACEABILITY_INDEX_PATH: 0,
        INITIATIVE_INDEX_PATH: 0,
        COORDINATION_INDEX_PATH: 0,
    }
    original_load_json_object = ControlPlaneLoader.load_json_object

    def wrapped_load_json_object(
        self: ControlPlaneLoader,
        relative_path: str,
    ) -> dict[str, object]:
        if relative_path in source_read_counts:
            source_read_counts[relative_path] += 1
        return original_load_json_object(self, relative_path)

    monkeypatch.setattr(
        ControlPlaneLoader,
        "load_json_object",
        wrapped_load_json_object,
    )

    result = service.run()

    assert result.wrote is False
    assert source_read_counts == {
        TASK_INDEX_PATH: 0,
        TRACEABILITY_INDEX_PATH: 0,
        INITIATIVE_INDEX_PATH: 0,
        COORDINATION_INDEX_PATH: 0,
    }


def test_coordination_sync_dry_run_uses_generated_dependency_artifacts(
    coordination_fixture_repo: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = coordination_fixture_repo
    trace_id = _first_live_initiative_trace_id(repo_root)
    initiative_index_path = repo_root / INITIATIVE_INDEX_PATH
    initiative_index = json.loads(initiative_index_path.read_text(encoding="utf-8"))
    for entry in initiative_index["entries"]:
        if entry["trace_id"] == trace_id:
            entry["next_action"] = "STALE SNAPSHOT MARKER"
            break
    initiative_index_path.write_text(
        f"{json.dumps(initiative_index, indent=2)}\n",
        encoding="utf-8",
    )
    coordination_index_path = repo_root / COORDINATION_INDEX_PATH
    coordination_index = json.loads(coordination_index_path.read_text(encoding="utf-8"))
    coordination_index["summary"] = "STALE SNAPSHOT MARKER"
    coordination_index_path.write_text(
        f"{json.dumps(coordination_index, indent=2)}\n",
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    service = CoordinationSyncService(loader)
    captured_content: dict[str, str] = {}
    original_build_document = CoordinationTrackingSyncService.build_document

    def wrapped_build_document(
        self: CoordinationTrackingSyncService,
    ):  # type: ignore[no-untyped-def]
        result = original_build_document(self)
        captured_content["content"] = result.content
        return result

    monkeypatch.setattr(
        CoordinationTrackingSyncService,
        "build_document",
        wrapped_build_document,
    )

    result = service.run()

    assert result.wrote is False
    assert "content" in captured_content
    assert "STALE SNAPSHOT MARKER" not in captured_content["content"]


def test_all_sync_can_materialize_to_output_dir(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = AllSyncService(loader)
    output_dir = tmp_path / "sync_all"

    result = service.run(output_dir=output_dir)

    assert result.wrote is True
    assert (output_dir / "core/control_plane/indexes/commands/command_index.json").exists()
    assert (output_dir / "core/control_plane/indexes/foundations/foundation_index.json").exists()
    assert (output_dir / "plan/.wt/indexes/initiative_index.json").exists()
    assert (output_dir / "plan/tracking/initiative_tracking.md").exists()


def test_coordination_sync_can_materialize_to_output_dir(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = CoordinationSyncService(loader)
    output_dir = tmp_path / "sync_coordination"

    result = service.run(output_dir=output_dir)

    assert result.wrote is True
    assert (output_dir / "plan/.wt/indexes/task_index.json").exists()
    assert (
        output_dir / "core/control_plane/indexes/traceability/traceability_index.json"
    ).exists()
    assert (output_dir / "plan/.wt/indexes/initiative_index.json").exists()
    assert (output_dir / "plan/.wt/indexes/coordination_index.json").exists()
    assert (output_dir / "plan/tracking/task_tracking.md").exists()
    assert (output_dir / "plan/tracking/initiative_tracking.md").exists()
    assert (output_dir / "plan/tracking/coordination_tracking.md").exists()


def test_coordination_sync_output_dir_uses_generated_dependency_artifacts(
    coordination_fixture_repo: Path,
    tmp_path: Path,
) -> None:
    repo_root = coordination_fixture_repo
    trace_id = _first_live_initiative_trace_id(repo_root)
    initiative_index_path = repo_root / INITIATIVE_INDEX_PATH
    initiative_index = json.loads(initiative_index_path.read_text(encoding="utf-8"))
    for entry in initiative_index["entries"]:
        if entry["trace_id"] == trace_id:
            entry["next_action"] = "STALE SNAPSHOT MARKER"
            break
    initiative_index_path.write_text(
        f"{json.dumps(initiative_index, indent=2)}\n",
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    service = CoordinationSyncService(loader)
    output_dir = tmp_path / "sync_coordination_overlay"

    result = service.run(output_dir=output_dir)

    tracker_path = output_dir / "plan/tracking/initiative_tracking.md"
    tracker_text = tracker_path.read_text(encoding="utf-8")
    coordination_index_path = output_dir / COORDINATION_INDEX_PATH
    coordination_text = coordination_index_path.read_text(encoding="utf-8")
    coordination_tracking_path = output_dir / "plan/tracking/coordination_tracking.md"
    coordination_tracking_text = coordination_tracking_path.read_text(encoding="utf-8")
    assert result.wrote is True
    assert trace_id in tracker_text
    assert "STALE SNAPSHOT MARKER" not in tracker_text
    assert "STALE SNAPSHOT MARKER" not in coordination_text
    assert "STALE SNAPSHOT MARKER" not in coordination_tracking_text


def test_all_sync_rejects_document_targets_without_entries_list() -> None:
    class BrokenDocumentService:
        def build_document(self) -> dict[str, object]:
            return {"id": "index.broken"}

        def write_document(
            self,
            document: dict[str, object],
            destination: Path | None = None,
        ) -> Path:
            raise AssertionError("Broken document targets should fail before write_document runs.")

    loader = ControlPlaneLoader(REPO_ROOT)
    service = AllSyncService(loader)

    with pytest.raises(RuntimeError, match="broken-index document is missing its entries list"):
        service._run_document_sync(
            loader=loader,
            target="broken-index",
            artifact_kind="index",
            relative_output_path="core/control_plane/indexes/broken/broken_index.json",
            service=BrokenDocumentService(),
            write=False,
            output_dir=None,
        )


def test_all_sync_rejects_unvalidated_document_overrides() -> None:
    class BrokenDocumentService:
        def build_document(self) -> dict[str, object]:
            return {"entries": []}

        def write_document(
            self,
            document: dict[str, object],
            destination: Path | None = None,
        ) -> Path:
            raise AssertionError("Broken document targets should fail before write_document runs.")

    loader = ControlPlaneLoader(REPO_ROOT)
    service = AllSyncService(loader)
    broken_output_path = "core/control_plane/indexes/broken/broken_index.json"

    with pytest.raises(
        SchemaResolutionError,
        match="No published schema ID was provided for validation",
    ):
        service._run_document_sync(
            loader=loader,
            target="broken-index",
            artifact_kind="index",
            relative_output_path=broken_output_path,
            service=BrokenDocumentService(),
            write=False,
            output_dir=None,
        )

    with pytest.raises(ArtifactLoadError, match=broken_output_path):
        loader.load_json_object(broken_output_path)
