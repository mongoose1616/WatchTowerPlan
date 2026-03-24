"""Runtime handlers for local release-gate commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _emit_detail_result, _run_value_error_operation
from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.pack_integration.release_check import (
    ReleaseCheckRequest,
    ReleaseCheckResult,
    run_release_check,
)
from watchtower_core.telemetry import telemetry_operation


def _run_release_check(args: argparse.Namespace) -> int:
    command_name = "watchtower-core release check"
    result = _run_value_error_operation(
        args,
        command_name=command_name,
        prefix="Release check error",
        operation=lambda: _run_release_check_operation(args),
    )
    if result is None:
        return 1

    payload = _build_release_check_payload(command_name=command_name, result=result)
    if result.dirty_worktree_blocked:
        payload["status"] = "error"
        payload["message"] = (
            "Git worktree is dirty. Commit or stash unrelated changes before release, "
            "or rerun with --allow-dirty for a local rehearsal."
        )

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=lambda: _print_release_check_summary(result),
        exit_code=0 if result.passed else 1,
    )


def _run_release_check_operation(args: argparse.Namespace) -> ReleaseCheckResult:
    loader = ControlPlaneLoader()
    pack_settings_path = getattr(args, "pack_settings_path", None) or PACK_SETTINGS_PATH
    with telemetry_operation(
        "release",
        "check",
        attributes={
            "output_root": str(args.output_root),
            "included_pack_slugs": tuple(args.include_pack or ()),
            "pack_only": bool(args.pack_only),
            "schema_paths": tuple(args.schema_path or ()),
            "allow_dirty": bool(args.allow_dirty),
            "pack_settings_path": pack_settings_path,
        },
    ) as operation:
        result = run_release_check(
            loader.repo_root,
            ReleaseCheckRequest(
                output_root=args.output_root,
                included_pack_slugs=tuple(args.include_pack or ()),
                overwrite=bool(args.overwrite),
                pack_only=bool(args.pack_only),
                allow_dirty=bool(args.allow_dirty),
                schema_paths=tuple(args.schema_path or ()),
                pack_settings_path=pack_settings_path,
            ),
        )
        if operation is not None:
            operation.set_result(
                status="ok" if result.passed else "failed",
                dirty_worktree_blocked=result.dirty_worktree_blocked,
                validation_all_failed=(
                    False
                    if result.validation_all_result is None
                    else not result.validation_all_result.passed
                ),
                schema_validation_count=len(result.schema_validations),
                export_scope=result.export_scope,
                portability_issue_count=(
                    None
                    if result.export_result is None
                    else result.export_result.portability_result.issue_count
                ),
            )
    return result


def _build_release_check_payload(
    *,
    command_name: str,
    result: ReleaseCheckResult,
) -> dict[str, object]:
    validation_all = result.validation_all_result
    export_result = result.export_result
    return {
        "command": command_name,
        "status": "ok",
        "passed": result.passed,
        "output_root": result.output_root,
        "export_scope": result.export_scope,
        "included_pack_slugs": list(result.included_pack_slugs),
        "allow_dirty": result.allow_dirty,
        "dirty_worktree_blocked": result.dirty_worktree_blocked,
        "pack_settings_path": result.pack_settings_path,
        "worktree": {
            "available": result.worktree.available,
            "clean": result.worktree.clean,
            "repo_root": result.worktree.repo_root,
            "git_root": result.worktree.git_root,
            "tracked_change_count": result.worktree.tracked_change_count,
            "untracked_change_count": result.worktree.untracked_change_count,
            "message": result.worktree.message,
            "entries": [
                {
                    "raw_status": entry.raw_status,
                    "path": entry.path,
                    "original_path": entry.original_path,
                    "tracked": entry.tracked,
                }
                for entry in result.worktree.entries
            ],
        },
        "requested_schema_paths": list(result.requested_schema_paths),
        "auto_detected_schema_paths": list(result.auto_detected_schema_paths),
        "schema_validations": [
            {
                "schema_path": summary.schema_path,
                "auto_detected": summary.auto_detected,
                "passed": summary.result.passed,
                "validator_id": summary.result.validator_id,
                "target_path": summary.result.target_path,
                "schema_ids": list(summary.result.schema_ids),
                "issue_count": summary.result.issue_count,
                "issues": [
                    {
                        "code": issue.code,
                        "message": issue.message,
                        "location": issue.location,
                        "schema_id": issue.schema_id,
                    }
                    for issue in summary.result.issues
                ],
            }
            for summary in result.schema_validations
        ],
        "validation_all": (
            None
            if validation_all is None
            else {
                "passed": validation_all.passed,
                "total_count": validation_all.total_count,
                "passed_count": validation_all.passed_count,
                "failed_count": validation_all.failed_count,
                "included_families": list(validation_all.included_families),
                "family_summaries": [
                    {
                        "family": summary.family,
                        "total_count": summary.total_count,
                        "passed_count": summary.passed_count,
                        "failed_count": summary.failed_count,
                    }
                    for summary in validation_all.family_summaries
                ],
            }
        ),
        "export": (
            None
            if export_result is None
            else {
                "passed": export_result.passed,
                "output_root": export_result.output_root,
                "export_scope": export_result.export_scope,
                "included_pack_slugs": list(export_result.included_pack_slugs),
                "default_pack_slug": export_result.default_pack_slug,
                "copied_paths": list(export_result.copied_paths),
                "scrubbed_paths": list(export_result.scrubbed_paths),
                "changed_paths": list(export_result.changed_paths),
                "workspace_lock_removed": export_result.workspace_lock_removed,
                "pack_validation_note": export_result.pack_validation_note,
                "pack_validations": [
                    {
                        "pack_slug": summary.pack_slug,
                        "pack_settings_path": summary.pack_settings_path,
                        "passed": summary.passed,
                        "issue_count": summary.issue_count,
                        "issues": [
                            {
                                "code": issue.code,
                                "message": issue.message,
                                "location": issue.location,
                                "schema_id": issue.schema_id,
                            }
                            for issue in summary.issues
                        ],
                    }
                    for summary in export_result.pack_validations
                ],
                "portability": {
                    "passed": export_result.portability_result.passed,
                    "validator_id": export_result.portability_result.validator_id,
                    "target_path": export_result.portability_result.target_path,
                    "schema_ids": list(export_result.portability_result.schema_ids),
                    "issue_count": export_result.portability_result.issue_count,
                    "issues": [
                        {
                            "code": issue.code,
                            "message": issue.message,
                            "location": issue.location,
                            "schema_id": issue.schema_id,
                        }
                        for issue in export_result.portability_result.issues
                    ],
                },
            }
        ),
    }


def _print_release_check_summary(result: ReleaseCheckResult) -> int:
    print("PASS" if result.passed else "FAIL", "release check")
    print(f"Output Root: {result.output_root}")
    print(f"Export Scope: {result.export_scope}")
    if result.included_pack_slugs:
        print("Included Packs: " + ", ".join(result.included_pack_slugs))
    print(
        "Git Worktree: "
        + (
            f"unavailable ({result.worktree.message})"
            if not result.worktree.available
            else ("clean" if result.worktree.clean else "dirty")
        )
    )
    if result.worktree.available and result.worktree.entries:
        for entry in result.worktree.entries:
            original = f" (from {entry.original_path})" if entry.original_path else ""
            print(f"- {entry.raw_status} {entry.path}{original}")
    if result.dirty_worktree_blocked:
        print(
            "Git worktree is dirty. Commit or stash unrelated changes before release, "
            "or rerun with --allow-dirty for a local rehearsal."
        )
        return 1

    if result.validation_all_result is not None:
        print(
            "Validate All: "
            f"{result.validation_all_result.passed_count}/"
            f"{result.validation_all_result.total_count} passed"
        )
    if result.schema_validations:
        print(
            "Schema Checks: "
            + ", ".join(
                f"{summary.schema_path}={'pass' if summary.result.passed else 'fail'}"
                for summary in result.schema_validations
            )
        )
    if result.export_result is not None:
        print(
            "Portability: "
            f"{result.export_result.portability_result.issue_count} issue(s)"
        )
        if result.export_result.pack_validations:
            print(
                "Pack Validations: "
                + ", ".join(
                    f"{summary.pack_slug}={'pass' if summary.passed else 'fail'}"
                    for summary in result.export_result.pack_validations
                )
            )
    if result.passed:
        print("Release gate passed and the staged export is ready for handoff.")
        return 0
    print("Release gate failed. Inspect the validation or export results above.")
    return 1
