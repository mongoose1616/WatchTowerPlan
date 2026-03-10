"""Runtime handlers for sync command families."""

from __future__ import annotations

import argparse
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Protocol

from watchtower_core.cli.handler_common import _print_payload, _resolve_output_path
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync import (
    AllSyncService,
    CommandIndexSyncService,
    CoordinationSyncService,
    DecisionIndexSyncService,
    DecisionTrackingSyncService,
    DesignDocumentIndexSyncService,
    DesignTrackingSyncService,
    FoundationIndexSyncService,
    GitHubTaskSyncParams,
    GitHubTaskSyncService,
    InitiativeIndexSyncService,
    InitiativeTrackingSyncService,
    PrdIndexSyncService,
    PrdTrackingSyncService,
    ReferenceIndexSyncService,
    RepositoryPathIndexSyncService,
    StandardIndexSyncService,
    TaskIndexSyncService,
    TaskTrackingSyncService,
    TraceabilityIndexSyncService,
    WorkflowIndexSyncService,
)


class _DocumentSyncService(Protocol):
    def build_document(self) -> dict[str, Any]:
        """Build the artifact document."""

    def write_document(
        self,
        document: Mapping[str, Any],
        destination: Path | None = None,
    ) -> Path:
        """Write the artifact document."""


def _run_sync_repository_paths(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync repository-paths",
        artifact_label="repository path index",
        service=RepositoryPathIndexSyncService.from_repo_root(),
    )


def _run_sync_command_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync command-index",
        artifact_label="command index",
        service=CommandIndexSyncService.from_repo_root(),
    )


def _run_sync_all(args: argparse.Namespace) -> int:
    service = AllSyncService.from_repo_root()
    result = service.run(write=args.write, output_dir=args.output_dir)
    payload = {
        "command": "watchtower-core sync all",
        "status": "ok",
        "result_count": len(result.records),
        "wrote": result.wrote,
        "output_dir": result.output_dir,
        "results": [
            {
                "target": record.target,
                "artifact_kind": record.artifact_kind,
                "relative_output_path": record.relative_output_path,
                "output_path": record.output_path,
                "wrote": record.wrote,
                "record_count": record.record_count,
                "details": record.details,
            }
            for record in result.records
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    mode = (
        f"output-dir mode at {result.output_dir}"
        if result.output_dir is not None
        else ("write mode" if result.wrote else "dry-run mode")
    )
    print(f"Ran sync all across {len(result.records)} targets in {mode}.")
    for record in result.records:
        print(
            f"- {record.target} [{record.artifact_kind}] "
            f"record_count={record.record_count}"
        )
        if record.output_path is not None:
            print(f"  Wrote to {record.output_path}")
    return 0


def _run_sync_coordination(args: argparse.Namespace) -> int:
    service = CoordinationSyncService.from_repo_root()
    result = service.run(write=args.write, output_dir=args.output_dir)
    payload = {
        "command": "watchtower-core sync coordination",
        "status": "ok",
        "result_count": len(result.records),
        "wrote": result.wrote,
        "output_dir": result.output_dir,
        "results": [
            {
                "target": record.target,
                "artifact_kind": record.artifact_kind,
                "relative_output_path": record.relative_output_path,
                "output_path": record.output_path,
                "wrote": record.wrote,
                "record_count": record.record_count,
                "details": record.details,
            }
            for record in result.records
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    mode = (
        f"output-dir mode at {result.output_dir}"
        if result.output_dir is not None
        else ("write mode" if result.wrote else "dry-run mode")
    )
    print(f"Ran sync coordination across {len(result.records)} targets in {mode}.")
    for record in result.records:
        print(
            f"- {record.target} [{record.artifact_kind}] "
            f"record_count={record.record_count}"
        )
        if record.output_path is not None:
            print(f"  Wrote to {record.output_path}")
    return 0


def _run_sync_reference_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync reference-index",
        artifact_label="reference index",
        service=ReferenceIndexSyncService.from_repo_root(),
    )


def _run_sync_foundation_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync foundation-index",
        artifact_label="foundation index",
        service=FoundationIndexSyncService.from_repo_root(),
    )


def _run_sync_standard_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync standard-index",
        artifact_label="standard index",
        service=StandardIndexSyncService.from_repo_root(),
    )


def _run_sync_prd_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync prd-index",
        artifact_label="PRD index",
        service=PrdIndexSyncService.from_repo_root(),
    )


def _run_sync_prd_tracking(args: argparse.Namespace) -> int:
    service = PrdTrackingSyncService.from_repo_root()
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": "watchtower-core sync prd-tracking",
        "status": "ok",
        "prd_count": result.prd_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content
    if _print_payload(args, payload) == 0:
        return 0

    if wrote:
        print(
            f"Rebuilt PRD tracking with {result.prd_count} entries and wrote it to {destination}."
        )
        return 0

    print(f"Rebuilt PRD tracking with {result.prd_count} entries in dry-run mode.")
    print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")
    return 0


def _run_sync_decision_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync decision-index",
        artifact_label="decision index",
        service=DecisionIndexSyncService.from_repo_root(),
    )


def _run_sync_decision_tracking(args: argparse.Namespace) -> int:
    service = DecisionTrackingSyncService.from_repo_root()
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": "watchtower-core sync decision-tracking",
        "status": "ok",
        "decision_count": result.decision_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content
    if _print_payload(args, payload) == 0:
        return 0

    if wrote:
        print(
            "Rebuilt decision tracking with "
            f"{result.decision_count} entries and wrote it to {destination}."
        )
        return 0

    print(f"Rebuilt decision tracking with {result.decision_count} entries in dry-run mode.")
    print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")
    return 0


def _run_sync_design_document_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync design-document-index",
        artifact_label="design-document index",
        service=DesignDocumentIndexSyncService.from_repo_root(),
    )


def _run_sync_design_tracking(args: argparse.Namespace) -> int:
    service = DesignTrackingSyncService.from_repo_root()
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": "watchtower-core sync design-tracking",
        "status": "ok",
        "feature_design_count": result.feature_design_count,
        "implementation_plan_count": result.implementation_plan_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content
    if _print_payload(args, payload) == 0:
        return 0

    total = result.feature_design_count + result.implementation_plan_count
    if wrote:
        print(f"Rebuilt design tracking with {total} documents and wrote it to {destination}.")
        return 0

    print(f"Rebuilt design tracking with {total} documents in dry-run mode.")
    print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")
    return 0


def _run_sync_initiative_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync initiative-index",
        artifact_label="initiative index",
        service=InitiativeIndexSyncService.from_repo_root(),
    )


def _run_sync_initiative_tracking(args: argparse.Namespace) -> int:
    service = InitiativeTrackingSyncService.from_repo_root()
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": "watchtower-core sync initiative-tracking",
        "status": "ok",
        "initiative_count": result.initiative_count,
        "active_count": result.active_count,
        "closed_count": result.closed_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content
    if _print_payload(args, payload) == 0:
        return 0

    if wrote:
        print(
            "Rebuilt initiative tracking with "
            f"{result.initiative_count} initiatives and wrote it to {destination}."
        )
        return 0

    print(
        "Rebuilt initiative tracking with "
        f"{result.initiative_count} initiatives in dry-run mode."
    )
    print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")
    return 0


def _run_sync_task_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync task-index",
        artifact_label="task index",
        service=TaskIndexSyncService.from_repo_root(),
    )


def _run_sync_task_tracking(args: argparse.Namespace) -> int:
    service = TaskTrackingSyncService.from_repo_root()
    result = service.build_document()
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(result, target))
        wrote = True

    payload: dict[str, object] = {
        "command": "watchtower-core sync task-tracking",
        "status": "ok",
        "task_count": result.task_count,
        "open_count": result.open_count,
        "closed_count": result.closed_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = result.content
    if _print_payload(args, payload) == 0:
        return 0

    if wrote:
        print(
            f"Rebuilt task tracking with {result.task_count} tasks and wrote it to {destination}."
        )
        return 0

    print(f"Rebuilt task tracking with {result.task_count} tasks in dry-run mode.")
    print("Use --write to update the canonical tracker or --output <path> to write elsewhere.")
    return 0


def _run_sync_github_tasks(args: argparse.Namespace) -> int:
    service = GitHubTaskSyncService(ControlPlaneLoader())
    result = service.sync(
        GitHubTaskSyncParams(
            task_ids=tuple(args.task_id),
            trace_id=args.trace_id,
            task_status=args.task_status,
            priority=args.priority,
            owner=args.owner,
            task_kind=args.task_kind,
            blocked_only=args.blocked_only,
            blocked_by_task_id=args.blocked_by,
            depends_on_task_id=args.depends_on,
            repository=args.repo,
            project_owner=args.project_owner,
            project_owner_type=args.project_owner_type,
            project_number=args.project_number,
            project_status_field_name=args.project_status_field,
            token_env=args.token_env,
            sync_labels=not args.no_label_sync,
        ),
        write=args.write,
    )
    payload = {
        "command": "watchtower-core sync github-tasks",
        "status": "ok" if all(record.success for record in result.records) else "error",
        "wrote": result.wrote,
        "result_count": len(result.records),
        "synced_task_count": result.synced_task_count,
        "local_change_count": result.local_change_count,
        "rebuilt_task_index": result.rebuilt_task_index,
        "rebuilt_task_tracking": result.rebuilt_task_tracking,
        "rebuilt_traceability_index": result.rebuilt_traceability_index,
        "results": [
            {
                "task_id": record.task_id,
                "doc_path": record.doc_path,
                "repository": record.repository,
                "task_status": record.task_status,
                "issue_action": record.issue_action,
                "project_action": record.project_action,
                "success": record.success,
                "message": record.message,
                "github_issue_number": record.github_issue_number,
                "github_issue_url": record.github_issue_url,
                "github_project_item_id": record.github_project_item_id,
                "labels": list(record.labels),
            }
            for record in result.records
        ],
    }
    exit_code = 0 if payload["status"] == "ok" else 1
    if _print_payload(args, payload) == 0:
        return exit_code

    if not result.records:
        print("No task entries matched the requested sync filters.")
        return 0
    for record in result.records:
        state = "ok" if record.success else "error"
        print(f"- {record.task_id} [{state}]")
        print(f"  Issue action: {record.issue_action}")
        if record.project_action is not None:
            print(f"  Project action: {record.project_action}")
        if record.labels:
            print(f"  Labels: {', '.join(record.labels)}")
        if record.github_issue_url is not None:
            print(f"  GitHub Issue: {record.github_issue_url}")
        print(f"  {record.message}")
    return exit_code


def _run_sync_traceability_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync traceability-index",
        artifact_label="traceability index",
        service=TraceabilityIndexSyncService.from_repo_root(),
    )


def _run_sync_workflow_index(args: argparse.Namespace) -> int:
    return _run_sync_document_command(
        args,
        command_name="watchtower-core sync workflow-index",
        artifact_label="workflow index",
        service=WorkflowIndexSyncService.from_repo_root(),
    )


def _run_sync_document_command(
    args: argparse.Namespace,
    *,
    command_name: str,
    artifact_label: str,
    service: _DocumentSyncService,
) -> int:
    document = service.build_document()
    entries = document.get("entries")
    if not isinstance(entries, list):
        raise RuntimeError(f"{artifact_label.capitalize()} document is missing its entries list.")
    entry_count = len(entries)
    destination: str | None = None
    wrote = False

    if args.write or args.output is not None:
        target = _resolve_output_path(args.output)
        destination = str(service.write_document(document, target))
        wrote = True

    payload: dict[str, object] = {
        "command": command_name,
        "status": "ok",
        "entry_count": entry_count,
        "wrote": wrote,
        "artifact_path": destination,
    }
    if args.include_document:
        payload["document"] = document
    if _print_payload(args, payload) == 0:
        return 0

    if wrote:
        print(f"Rebuilt {artifact_label} with {entry_count} entries and wrote it to {destination}.")
        return 0

    print(f"Rebuilt {artifact_label} with {entry_count} entries in dry-run mode.")
    print("Use --write to update the canonical artifact or --output <path> to write elsewhere.")
    return 0
