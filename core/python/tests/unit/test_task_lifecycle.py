from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest
from fixture_repo_support import materialize_governed_applies_to_targets

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops import task_documents as task_documents_module
from watchtower_core.repo_ops.task_lifecycle import (
    TaskCreateParams,
    TaskLifecycleService,
    TaskUpdateParams,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    copytree(REPO_ROOT / "docs" / "planning", repo_root / "docs" / "planning")
    (repo_root / "core" / "python").mkdir(parents=True)
    materialize_governed_applies_to_targets(repo_root)
    return repo_root


def test_task_create_can_recommend_closeout_for_terminal_single_trace(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    result = service.create(
        TaskCreateParams(
            task_id="task.unit_test_trace.done.001",
            trace_id="trace.unit_test_trace_done",
            title="Complete the trace",
            summary="Creates the final terminal task for a new trace.",
            task_kind="feature",
            priority="medium",
            owner="repository_maintainer",
            task_status="done",
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
    assert result.doc_path == "docs/planning/tasks/closed/unit_test_trace_done.md"


def test_task_create_canonicalizes_directory_applies_to_paths(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    result = service.create(
        TaskCreateParams(
            task_id="task.unit_test_trace.applies_to.001",
            trace_id="trace.unit_test_trace_applies_to",
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
    written_text = (repo_root / result.doc_path).read_text(encoding="utf-8")
    assert '- "core/python/tests/unit"' not in written_text
    assert "- core/python/tests/unit/" in written_text


def test_task_update_can_move_task_and_clear_optional_fields(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    service = TaskLifecycleService(loader)

    created = service.create(
        TaskCreateParams(
            task_id="task.unit_test_trace.lifecycle.001",
            trace_id="trace.unit_test_trace_lifecycle",
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
            task_status="done",
            clear_trace_id=True,
            clear_applies_to=True,
            clear_related_ids=True,
            scope_items=("Confirm the final state.",),
            done_when_items=("The task moved to closed.",),
            file_stem="lifecycle_task_complete",
            updated_at="2026-03-11T00:00:00Z",
        ),
        write=True,
    )

    assert result.changed is True
    assert result.moved is True
    assert result.wrote is True
    assert result.previous_doc_path == "docs/planning/tasks/open/lifecycle_task.md"
    assert result.doc_path == "docs/planning/tasks/closed/lifecycle_task_complete.md"
    assert not (repo_root / result.previous_doc_path).exists()

    written_text = (repo_root / result.doc_path).read_text(encoding="utf-8")
    assert "trace_id:" not in written_text
    assert "applies_to:" not in written_text
    assert "related_ids:" not in written_text
    assert "Lifecycle task complete" in written_text
    assert "The task is now complete." in written_text

    coordination_index_path = (
        repo_root / "core/control_plane/indexes/coordination/coordination_index.v1.json"
    )
    coordination_index = json.loads(coordination_index_path.read_text(encoding="utf-8"))
    assert coordination_index["status"] == "active"


def test_task_update_write_tolerates_other_task_disappearing_during_sync(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    service = TaskLifecycleService(loader)

    created = service.create(
        TaskCreateParams(
            task_id="task.unit_test_trace.disappearing_sync.001",
            trace_id="trace.unit_test_trace_disappearing_sync",
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
        for document in task_documents_module.iter_task_documents(loader)
        if document.task_id != created.task_id
    )
    original_loader = task_documents_module.load_task_document
    triggered = False

    def _load_task_document(loader_arg: ControlPlaneLoader, relative_path: str):
        nonlocal triggered
        if relative_path == missing_relative_path and not triggered:
            triggered = True
            raise FileNotFoundError(relative_path)
        return original_loader(loader_arg, relative_path)

    monkeypatch.setattr(task_documents_module, "load_task_document", _load_task_document)

    result = service.update(
        TaskUpdateParams(
            task_id=created.task_id,
            task_status="done",
            updated_at="2026-03-11T00:00:00Z",
        ),
        write=True,
    )

    assert triggered is True
    assert result.wrote is True
    assert result.doc_path == "docs/planning/tasks/closed/disappearing_sync_task.md"
    assert (repo_root / result.doc_path).exists()


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
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    with pytest.raises(
        ValueError,
        match="blocked_by cannot reference the current task: task.unit_test_trace.self.001",
    ):
        service.create(
            TaskCreateParams(
                task_id="task.unit_test_trace.self.001",
                trace_id="trace.unit_test_trace_self",
                title="Self reference",
                summary="A task with an invalid self reference.",
                task_kind="feature",
                priority="medium",
                owner="repository_maintainer",
                scope_items=("Create the task.",),
                done_when_items=("The task exists.",),
                blocked_by=("task.unit_test_trace.self.001",),
            ),
            write=False,
        )


def test_task_create_rejects_traced_related_ids_without_trace_id(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    with pytest.raises(
        ValueError,
        match="links to traced related_ids but is missing trace_id",
    ):
        service.create(
            TaskCreateParams(
                task_id="task.unit_test_trace.trace_linkage.001",
                title="Reject missing traced linkage",
                summary="Rejects traced related_ids without an explicit trace_id.",
                task_kind="feature",
                priority="medium",
                owner="repository_maintainer",
                scope_items=("Attempt invalid task creation.",),
                done_when_items=("The command fails closed.",),
                related_ids=("trace.unit_test_trace_trace_linkage",),
            ),
            write=False,
        )


def test_task_update_rejects_clearing_trace_id_while_traced_related_ids_remain(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    service = TaskLifecycleService(loader)
    created = service.create(
        TaskCreateParams(
            task_id="task.unit_test_trace.trace_linkage.002",
            trace_id="trace.unit_test_trace_trace_linkage",
            title="Reject trace mismatch",
            summary="Rejects removing trace_id while traced related_ids remain.",
            task_kind="feature",
            priority="medium",
            owner="repository_maintainer",
            scope_items=("Create the traced task.",),
            done_when_items=("The task exists.",),
            related_ids=("trace.unit_test_trace_trace_linkage",),
            file_stem="trace_linkage_reject",
        ),
        write=True,
    )

    with pytest.raises(
        ValueError,
        match="links to traced related_ids but is missing trace_id",
    ):
        service.update(
            TaskUpdateParams(
                task_id=created.task_id,
                clear_trace_id=True,
            ),
            write=False,
        )
