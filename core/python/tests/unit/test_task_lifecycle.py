from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest

from tests.integration.fixture_repo_support import (
    bootstrap_packwide_initiative,
    materialize_governed_applies_to_targets,
    materialize_plan_runtime_pack,
    packwide_initiative_root,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.plan_runtime import plan_task_state
from watchtower_core.plan_runtime.plan_task_state import update_task_document
from watchtower_core.plan_runtime.task_lifecycle import (
    TaskCreateParams,
    TaskLifecycleService,
    TaskUpdateParams,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    (repo_root / "core" / "python" / "tests" / "unit").mkdir(parents=True, exist_ok=True)
    materialize_plan_runtime_pack(repo_root, REPO_ROOT)
    materialize_governed_applies_to_targets(repo_root)
    return repo_root


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


def test_task_create_can_recommend_closeout_for_terminal_single_trace(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    trace_id = "trace.unit_test_trace_done"
    _bootstrap_trace(repo_root, trace_id, approve=True)
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


def test_task_create_canonicalizes_directory_applies_to_paths(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    trace_id = "trace.unit_test_trace_applies_to"
    _bootstrap_trace(repo_root, trace_id)
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


def test_task_update_writes_in_place_and_clears_optional_fields(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    trace_id = "trace.unit_test_trace_lifecycle"
    _bootstrap_trace(repo_root, trace_id, approve=True)
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
            related_ids=("prd.unit_test_hardening_and_rebalancing",),
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
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    trace_id = "trace.unit_test_trace_disappearing_sync"
    _bootstrap_trace(repo_root, trace_id, approve=True)
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
    original_loader = plan_task_state.load_task_document
    triggered = False

    def _load_task_document(loader_arg: ControlPlaneLoader, relative_path: str):
        nonlocal triggered
        if relative_path == missing_relative_path and not triggered:
            triggered = True
            raise FileNotFoundError(relative_path)
        return original_loader(loader_arg, relative_path)

    monkeypatch.setattr(plan_task_state, "load_task_document", _load_task_document)

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


def test_task_update_rejects_execution_start_before_initiative_approval(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    trace_id = "trace.unit_test_trace_execution_gate"
    _bootstrap_trace(repo_root, trace_id)
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


def test_task_update_rejects_conflicting_clear_flags(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
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


def test_task_create_rejects_self_reference(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    trace_id = "trace.unit_test_trace_self"
    _bootstrap_trace(repo_root, trace_id)
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


def test_task_create_rejects_mismatched_traced_related_ids(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    trace_id = "trace.unit_test_trace_trace_linkage"
    _bootstrap_trace(repo_root, trace_id)
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    with pytest.raises(
        ValueError,
        match="must match one of its traced related_ids",
    ):
        service.create(
            TaskCreateParams(
                task_id="task.unit_test_trace_trace_linkage.001",
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


def test_task_update_rejects_clearing_trace_id_for_live_task_state(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    trace_id = "trace.unit_test_trace_trace_linkage"
    _bootstrap_trace(repo_root, trace_id)
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
