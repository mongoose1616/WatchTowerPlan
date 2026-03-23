from __future__ import annotations

from pathlib import Path
from shutil import copytree

from watchtower_core.control_plane.event_stream import (
    EventStreamDescriptor,
    EventStreamHelper,
    EventStreamWriteRequest,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.workspace import WorkspaceConfig

REPO_ROOT = Path(__file__).resolve().parents[4]
PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    copytree(REPO_ROOT / "plan", repo_root / "plan")
    return repo_root


def test_event_stream_helper_builds_and_replays_initiative_events(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(
        workspace_config=WorkspaceConfig(
            repo_root=repo_root,
            control_plane_root=repo_root / "core" / "control_plane",
            python_workspace_root=repo_root / "core" / "python",
        )
    )
    helper = EventStreamHelper.from_loader(
        loader,
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )
    descriptor = EventStreamDescriptor.initiative(
        relative_dir="plan/initiatives/unit_event_stream/.wt/events",
        event_id_prefix="event.unit_event_stream",
        initiative_id="initiative.unit_event_stream",
        trace_id="trace.unit_event_stream",
    )

    seed_documents = helper.build_seed_documents(
        descriptor,
        (
            EventStreamWriteRequest(
                event_type="created",
                actor_id="actor.watchtower_core",
                recorded_at="2026-03-17T23:00:00Z",
                summary="Created the unit initiative stream.",
                related_paths=("plan/initiatives/unit_event_stream/initiative_brief.md",),
                payload={"task_count": 1},
            ),
            EventStreamWriteRequest(
                event_type="scope_defined",
                actor_id="actor.watchtower_core",
                recorded_at="2026-03-17T23:01:00Z",
                summary="Defined the unit initiative scope.",
                related_paths=("plan/initiatives/unit_event_stream/design_record.md",),
                payload={"scope_type": "pack_wide"},
            ),
        ),
    )
    for relative_path, document in seed_documents.items():
        loader.artifact_store.write_json_object(relative_path, document)

    helper.append_event(
        descriptor,
        EventStreamWriteRequest(
            event_type="ready_for_review_marked",
            actor_id="actor.repository_maintainer",
            recorded_at="2026-03-17T23:02:00Z",
            summary="Marked the unit initiative ready for review.",
            payload={},
        ),
    )

    replayed = helper.replay(descriptor)

    assert [document["sequence"] for document in replayed] == [1, 2, 3]
    assert replayed[0]["related_paths"] == [
        "plan/initiatives/unit_event_stream/initiative_brief.md"
    ]
    assert replayed[-1]["event_type"] == "ready_for_review_marked"
    assert helper.next_sequence(descriptor) == 4


def test_event_stream_helper_builds_and_replays_task_events(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(
        workspace_config=WorkspaceConfig(
            repo_root=repo_root,
            control_plane_root=repo_root / "core" / "control_plane",
            python_workspace_root=repo_root / "core" / "python",
        )
    )
    helper = EventStreamHelper.from_loader(
        loader,
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )
    descriptor = EventStreamDescriptor.task(
        relative_dir="plan/initiatives/unit_event_stream/.wt/tasks/example/events",
        event_id_prefix="event.unit_event_stream.example",
        initiative_id="initiative.unit_event_stream",
        task_id="task.unit_event_stream.example",
    )

    helper.append_event(
        descriptor,
        EventStreamWriteRequest(
            event_type="created",
            actor_id="actor.watchtower_core",
            recorded_at="2026-03-17T23:10:00Z",
            summary="Created the unit task event stream.",
            payload={"status": "planned"},
        ),
    )
    helper.append_event(
        descriptor,
        EventStreamWriteRequest(
            event_type="completed",
            actor_id="actor.repository_maintainer",
            recorded_at="2026-03-17T23:11:00Z",
            summary="Completed the unit task event stream.",
            payload={"status": "completed"},
        ),
    )

    replayed = helper.replay(descriptor)

    assert [document["event_type"] for document in replayed] == ["created", "completed"]
    assert replayed[0]["task_id"] == "task.unit_event_stream.example"
    assert "related_paths" not in replayed[0]
