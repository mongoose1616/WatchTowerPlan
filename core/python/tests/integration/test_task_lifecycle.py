from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree
from types import SimpleNamespace

import pytest
from watchtower_plan.initiatives import InitiativePackageService
from watchtower_plan.tasks import (
    TaskCreateParams,
    TaskLifecycleService,
    TaskUpdateParams,
    update_task_document,
)
from watchtower_plan.tasks import lifecycle as task_lifecycle_module
from watchtower_plan.tasks import state as plan_task_state

from tests.fixture_repo_support import (
    bootstrap_packwide_initiative,
    materialize_governed_applies_to_targets,
    materialize_minimal_plan_pack,
    packwide_initiative_root,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader

REPO_ROOT = Path(__file__).resolve().parents[4]
CAPTURE_TRACE_ID = "trace.task_lifecycle_capture"
APPROVED_TRACE_ID = "trace.task_lifecycle_ready"


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    (repo_root / "core" / "python" / "tests" / "unit").mkdir(parents=True, exist_ok=True)
    materialize_minimal_plan_pack(repo_root, REPO_ROOT)
    materialize_governed_applies_to_targets(repo_root, REPO_ROOT)
    loader = ControlPlaneLoader(repo_root)
    task_lifecycle_module.PlanWorkspaceService(loader).sync(write=True)
    task_lifecycle_module.CoordinationSyncService(loader).run(write=True)
    return repo_root


@pytest.fixture(scope="module")
def task_lifecycle_fixture_baseline(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return _build_fixture_repo(tmp_path_factory.mktemp("task_lifecycle_fixture_baseline"))


@pytest.fixture
def task_lifecycle_fixture_repo(tmp_path: Path, task_lifecycle_fixture_baseline: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(task_lifecycle_fixture_baseline, repo_root)
    return repo_root


@pytest.fixture(scope="module")
def task_lifecycle_capture_baseline(
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    repo_root = _build_fixture_repo(tmp_path_factory.mktemp("task_lifecycle_capture_baseline"))
    _bootstrap_trace(repo_root, CAPTURE_TRACE_ID)
    return repo_root


@pytest.fixture(scope="module")
def task_lifecycle_approved_baseline(
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    repo_root = _build_fixture_repo(tmp_path_factory.mktemp("task_lifecycle_approved_baseline"))
    _bootstrap_trace(repo_root, APPROVED_TRACE_ID, approve=True)
    return repo_root


@pytest.fixture
def task_lifecycle_capture_repo(tmp_path: Path, task_lifecycle_capture_baseline: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(task_lifecycle_capture_baseline, repo_root)
    return repo_root


@pytest.fixture
def task_lifecycle_approved_repo(
    tmp_path: Path,
    task_lifecycle_approved_baseline: Path,
) -> Path:
    repo_root = tmp_path / "repo"
    copytree(task_lifecycle_approved_baseline, repo_root)
    return repo_root


@pytest.fixture
def disable_expensive_task_sync(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, bool]]:
    calls: list[tuple[str, bool]] = []

    class _FakePlanWorkspaceService:
        def __init__(self, loader: ControlPlaneLoader) -> None:
            self._loader = loader

        def sync(self, *, write: bool = False) -> None:
            calls.append(("workspace", write))

    class _FakeCoordinationSyncService:
        def __init__(self, loader: ControlPlaneLoader) -> None:
            self._loader = loader

        def run(
            self,
            *,
            write: bool = False,
            output_dir: Path | None = None,
        ) -> SimpleNamespace:
            calls.append(("coordination", write))
            return SimpleNamespace(records=(), wrote=write, output_dir=output_dir)

    monkeypatch.setattr(task_lifecycle_module, "PlanWorkspaceService", _FakePlanWorkspaceService)
    monkeypatch.setattr(
        task_lifecycle_module,
        "CoordinationSyncService",
        _FakeCoordinationSyncService,
    )
    return calls


def _bootstrap_trace(repo_root: Path, trace_id: str, *, approve: bool = False) -> None:
    bootstrap_packwide_initiative(
        repo_root,
        trace_id=trace_id,
        title=f"{trace_id} Fixture",
        summary="Seeds one live initiative package for task lifecycle unit coverage.",
        approve=approve,
    )


def _task_path(repo_root: Path, trace_id: str, slug: str) -> str:
    return (
        packwide_initiative_root(repo_root, trace_id)
        .joinpath(".wt", "tasks", slug, "task.json")
        .relative_to(repo_root)
        .as_posix()
    )


def _complete_seed_task(repo_root: Path, trace_id: str) -> None:
    update_task_document(
        ControlPlaneLoader(repo_root),
        _task_path(repo_root, trace_id, "seed_bootstrap"),
        updates={
            "task_status": "completed",
            "updated_at": "2026-03-10T23:58:00Z",
        },
    )


def test_task_create_can_recommend_closeout_for_terminal_single_trace(
    task_lifecycle_approved_repo: Path,
) -> None:
    repo_root = task_lifecycle_approved_repo
    trace_id = APPROVED_TRACE_ID
    _complete_seed_task(repo_root, trace_id)
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    result = service.create(
        TaskCreateParams(
            task_id="task.unit_test_trace_done.001",
            trace_id=trace_id,
            title="Complete the trace",
            summary="Creates the final terminal task for a live initiative package.",
            task_kind="feature",
            priority="medium",
            owner="repository_maintainer",
            task_status="completed",
            scope_items=("Create the task.",),
            done_when_items=("The task exists.",),
            file_stem="unit_test_trace_done",
            updated_at="2026-03-10T23:59:59Z",
        ),
        write=False,
    )

    assert result.changed is True
    assert result.wrote is False
    assert result.closeout_recommended is True
    assert result.doc_path == _task_path(repo_root, trace_id, "unit_test_trace_done")


def test_task_create_canonicalizes_directory_applies_to_paths(
    task_lifecycle_capture_repo: Path,
    disable_expensive_task_sync: list[tuple[str, bool]],
) -> None:
    repo_root = task_lifecycle_capture_repo
    trace_id = CAPTURE_TRACE_ID
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    result = service.create(
        TaskCreateParams(
            task_id="task.unit_test_trace_applies_to.001",
            trace_id=trace_id,
            title="Canonicalize applies_to",
            summary="Ensures task create writes canonical directory applies_to values.",
            task_kind="feature",
            priority="medium",
            owner="repository_maintainer",
            scope_items=("Create the task.",),
            done_when_items=("The task exists.",),
            applies_to=("core/python/tests/unit",),
            file_stem="canonical_applies_to",
            updated_at="2026-03-10T23:59:59Z",
        ),
        write=True,
    )

    assert result.wrote is True
    written_document = json.loads((repo_root / result.doc_path).read_text(encoding="utf-8"))
    assert written_document["applies_to"] == ["core/python/tests/unit/"]


def test_task_update_writes_in_place_and_clears_optional_fields(
    task_lifecycle_approved_repo: Path,
) -> None:
    repo_root = task_lifecycle_approved_repo
    trace_id = APPROVED_TRACE_ID
    loader = ControlPlaneLoader(repo_root)
    service = TaskLifecycleService(loader)

    created = service.create(
        TaskCreateParams(
            task_id="task.unit_test_trace_lifecycle.001",
            trace_id=trace_id,
            title="Lifecycle task",
            summary="A task that will be updated.",
            task_kind="feature",
            priority="high",
            owner="repository_maintainer",
            scope_items=("Create the task.",),
            done_when_items=("The task exists.",),
            applies_to=("core/python/tests/unit",),
            related_ids=("initiative.unit_test_hardening_and_rebalancing",),
            file_stem="lifecycle_task",
            updated_at="2026-03-10T23:59:59Z",
        ),
        write=True,
    )

    result = service.update(
        TaskUpdateParams(
            task_id=created.task_id,
            title="Lifecycle task complete",
            summary="The task is now complete.",
            task_status="completed",
            clear_applies_to=True,
            clear_related_ids=True,
            scope_items=("Confirm the final state.",),
            done_when_items=("The task is completed in place.",),
            updated_at="2026-03-11T00:00:00Z",
        ),
        write=True,
    )

    assert result.changed is True
    assert result.moved is False
    assert result.wrote is True
    assert result.previous_doc_path is None
    assert result.doc_path == created.doc_path

    written_document = json.loads((repo_root / result.doc_path).read_text(encoding="utf-8"))
    assert "applies_to" not in written_document
    assert "related_ids" not in written_document
    assert written_document["title"] == "Lifecycle task complete"
    assert written_document["summary"] == "The task is now complete."
    assert written_document["status"] == "active"
    assert written_document["task_status"] == "completed"
    assert written_document["scope_items"] == ["Confirm the final state."]
    assert written_document["done_when_items"] == ["The task is completed in place."]

    coordination_index_path = repo_root / "plan/.wt/indexes/coordination_index.json"
    coordination_index = json.loads(coordination_index_path.read_text(encoding="utf-8"))
    assert coordination_index["status"] == "active"


def test_task_update_write_tolerates_other_task_disappearing_during_scan(
    task_lifecycle_approved_repo: Path,
    monkeypatch: pytest.MonkeyPatch,
    disable_expensive_task_sync: list[tuple[str, bool]],
) -> None:
    repo_root = task_lifecycle_approved_repo
    trace_id = APPROVED_TRACE_ID
    _bootstrap_trace(repo_root, "trace.unit_test_trace_disappearing_sync_other")
    loader = ControlPlaneLoader(repo_root)
    service = TaskLifecycleService(loader)

    created = service.create(
        TaskCreateParams(
            task_id="task.unit_test_trace_disappearing_sync.001",
            trace_id=trace_id,
            title="Disappearing sync task",
            summary="A task that will be updated while another task disappears.",
            task_kind="feature",
            priority="high",
            owner="repository_maintainer",
            scope_items=("Create the task.",),
            done_when_items=("The task exists.",),
            file_stem="disappearing_sync_task",
            updated_at="2026-03-10T23:59:59Z",
        ),
        write=True,
    )

    missing_relative_path = next(
        document.relative_path
        for document in plan_task_state.iter_task_documents(loader)
        if document.task_id != created.task_id
    )
    original_load = ControlPlaneLoader.load_validated_document
    triggered = False

    def _load_validated_document(loader_arg: ControlPlaneLoader, relative_path: str):
        nonlocal triggered
        if relative_path == missing_relative_path and not triggered:
            triggered = True
            raise FileNotFoundError(relative_path)
        return original_load(loader_arg, relative_path)

    monkeypatch.setattr(
        ControlPlaneLoader,
        "load_validated_document",
        _load_validated_document,
    )

    result = service.update(
        TaskUpdateParams(
            task_id=created.task_id,
            task_status="completed",
            updated_at="2026-03-11T00:00:00Z",
        ),
        write=True,
    )

    assert triggered is True
    assert result.wrote is True
    assert result.doc_path == created.doc_path
    assert (repo_root / result.doc_path).exists()


def test_iter_task_documents_scans_initiative_state_once_per_pass(
    task_lifecycle_approved_repo: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    loader = ControlPlaneLoader(task_lifecycle_approved_repo)
    original_iter = plan_task_state.iter_initiative_states
    calls = 0

    def _iter_initiative_states(loader_arg: ControlPlaneLoader):
        nonlocal calls
        calls += 1
        return original_iter(loader_arg)

    monkeypatch.setattr(
        plan_task_state,
        "iter_initiative_states",
        _iter_initiative_states,
    )

    documents = plan_task_state.iter_task_documents(loader)

    assert documents
    assert calls == 1


def test_task_update_rejects_execution_start_before_initiative_approval(
    task_lifecycle_capture_repo: Path,
    disable_expensive_task_sync: list[tuple[str, bool]],
) -> None:
    repo_root = task_lifecycle_capture_repo
    trace_id = CAPTURE_TRACE_ID
    loader = ControlPlaneLoader(repo_root)
    service = TaskLifecycleService(loader)
    created = service.create(
        TaskCreateParams(
            task_id="task.unit_test_trace_execution_gate.001",
            trace_id=trace_id,
            title="Gate execution start",
            summary="Proves execution-status transitions fail before approval.",
            task_kind="feature",
            priority="high",
            owner="repository_maintainer",
            scope_items=("Create the gated task.",),
            done_when_items=("The task exists but has not started execution.",),
            file_stem="gate_execution_start",
        ),
        write=True,
    )

    with pytest.raises(
        ValueError,
        match="approved and marked ready_for_execution before execution starts",
    ):
        service.update(
            TaskUpdateParams(
                task_id=created.task_id,
                task_status="in_progress",
            ),
            write=False,
        )


def test_task_create_reloads_initiative_state_before_execution_write(
    task_lifecycle_capture_repo: Path,
    monkeypatch: pytest.MonkeyPatch,
    disable_expensive_task_sync: list[tuple[str, bool]],
) -> None:
    repo_root = task_lifecycle_capture_repo
    trace_id = CAPTURE_TRACE_ID
    initiative_slug = "task_lifecycle_capture"
    loader = ControlPlaneLoader(repo_root)
    stale_initiative = plan_task_state.find_initiative_by_trace_id(loader, trace_id)

    package_service = InitiativePackageService(loader)
    package_service.approve_packwide(
        initiative_slug,
        "actor.repository_maintainer",
        write=True,
    )

    original_resolve = task_lifecycle_module.find_initiative_by_trace_id

    def _return_stale_initiative(
        loader_arg: ControlPlaneLoader,
        requested_trace_id: str,
    ):
        if requested_trace_id == trace_id:
            return stale_initiative
        return original_resolve(loader_arg, requested_trace_id)

    monkeypatch.setattr(
        task_lifecycle_module,
        "find_initiative_by_trace_id",
        _return_stale_initiative,
    )
    service = TaskLifecycleService(loader)
    result = service.create(
        TaskCreateParams(
            task_id="task.unit_test_trace_stale_initiative_snapshot.001",
            trace_id=trace_id,
            title="Start execution from fresh initiative state",
            summary="Proves task lifecycle writes reload initiative state before mutation.",
            task_kind="feature",
            priority="high",
            owner="repository_maintainer",
            task_status="in_progress",
            scope_items=("Start execution after approval.",),
            done_when_items=("Execution has started without clobbering approval state.",),
            updated_at="2026-03-19T21:15:00Z",
        ),
        write=True,
    )

    state_path = packwide_initiative_root(repo_root, trace_id) / ".wt" / "initiative.json"
    initiative_state = json.loads(state_path.read_text(encoding="utf-8"))

    assert result.wrote is True
    assert initiative_state["gate_state"]["approval_status"] == "approved"
    assert initiative_state["gate_state"]["ready_for_execution"] is True
    assert initiative_state["review_status"] == "approved"
    assert initiative_state["lifecycle_stage"] == "in_progress"
    assert result.task_id in initiative_state["task_ids"]
    assert any(
        approval["approval_kind"] == "ready_for_execution"
        for approval in initiative_state["approvals"]
    )


def test_task_update_rejects_conflicting_clear_flags(task_lifecycle_fixture_repo: Path) -> None:
    repo_root = task_lifecycle_fixture_repo
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    with pytest.raises(
        ValueError,
        match="Cannot provide replacement values and clear depends_on in the same call.",
    ):
        service.update(
            TaskUpdateParams(
                task_id="task.local_task_tracking.github_sync.001",
                depends_on=("task.bootstrap.001",),
                clear_depends_on=True,
            ),
            write=False,
        )


def test_task_create_rejects_self_reference(task_lifecycle_capture_repo: Path) -> None:
    repo_root = task_lifecycle_capture_repo
    trace_id = CAPTURE_TRACE_ID
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    with pytest.raises(
        ValueError,
        match="blocked_by cannot reference the current task: task.unit_test_trace_self.001",
    ):
        service.create(
            TaskCreateParams(
                task_id="task.unit_test_trace_self.001",
                trace_id=trace_id,
                title="Self reference",
                summary="A task with an invalid self reference.",
                task_kind="feature",
                priority="medium",
                owner="repository_maintainer",
                scope_items=("Create the task.",),
                done_when_items=("The task exists.",),
                blocked_by=("task.unit_test_trace_self.001",),
            ),
            write=False,
        )


def test_task_create_rejects_mismatched_traced_related_ids(
    task_lifecycle_capture_repo: Path,
) -> None:
    repo_root = task_lifecycle_capture_repo
    trace_id = CAPTURE_TRACE_ID
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    with pytest.raises(
        ValueError,
        match="must match one of its traced related_ids",
    ):
        service.create(
            TaskCreateParams(
                task_id="task.unit_test_trace_trace_linkage.001",
                trace_id=trace_id,
                title="Reject mismatched traced linkage",
                summary="Rejects traced related_ids that point at a different trace.",
                task_kind="feature",
                priority="medium",
                owner="repository_maintainer",
                scope_items=("Attempt invalid task creation.",),
                done_when_items=("The command fails closed.",),
                related_ids=("trace.some_other_trace",),
            ),
            write=False,
        )


def test_task_update_rejects_clearing_trace_id_for_live_task_state(
    task_lifecycle_capture_repo: Path,
    disable_expensive_task_sync: list[tuple[str, bool]],
) -> None:
    repo_root = task_lifecycle_capture_repo
    trace_id = CAPTURE_TRACE_ID
    loader = ControlPlaneLoader(repo_root)
    service = TaskLifecycleService(loader)
    created = service.create(
        TaskCreateParams(
            task_id="task.unit_test_trace_trace_linkage.002",
            trace_id=trace_id,
            title="Reject trace clearing",
            summary="Rejects removing trace inheritance from a live task.",
            task_kind="feature",
            priority="medium",
            owner="repository_maintainer",
            scope_items=("Create the traced task.",),
            done_when_items=("The task exists.",),
            related_ids=(trace_id,),
            file_stem="trace_linkage_reject",
        ),
        write=True,
    )

    with pytest.raises(
        ValueError,
        match="cannot clear it",
    ):
        service.update(
            TaskUpdateParams(
                task_id=created.task_id,
                clear_trace_id=True,
            ),
            write=False,
        )
