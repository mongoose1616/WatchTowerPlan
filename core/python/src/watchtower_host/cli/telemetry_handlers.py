"""Runtime handlers for telemetry cleanup commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _emit_command_error, _emit_detail_result
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.telemetry import TelemetryCleanupService, TelemetryDeleteRequest


def _run_telemetry_delete(args: argparse.Namespace) -> int:
    loader = ControlPlaneLoader()

    try:
        result = TelemetryCleanupService(loader).delete(
            TelemetryDeleteRequest(
                pack_settings_path=args.pack_settings_path,
                telemetry_root=args.telemetry_root,
                older_than_days=args.older_than_days,
                before=args.before,
                delete_all=bool(args.all),
                write=bool(args.write),
            )
        )
    except (OSError, ValueError) as exc:
        return _emit_command_error(
            args,
            "watchtower-core telemetry delete",
            str(exc),
            prefix="Telemetry error",
        )

    payload = {
        "command": "watchtower-core telemetry delete",
        "status": "ok",
        "write": result.write,
        "selection_mode": result.selection_mode,
        "cutoff_utc": result.cutoff_utc,
        "telemetry_root": str(result.telemetry_root),
        "pack_settings_path": result.pack_settings_path,
        "machine_root": result.machine_root,
        "active_session_output_path": result.active_session_output_path,
        "matched_file_count": result.matched_file_count,
        "matched_directory_count": result.matched_directory_count,
        "matched_bytes": result.matched_bytes,
        "deleted_file_count": result.deleted_file_count,
        "deleted_directory_count": result.deleted_directory_count,
        "deleted_bytes": result.deleted_bytes,
        "matched_file_paths": list(result.matched_file_paths),
        "pruned_directory_paths": list(result.pruned_directory_paths),
    }

    def _render_human() -> None:
        verb = "Deleted" if result.write else "Would delete"
        print(f"{verb} telemetry under: {result.telemetry_root}")
        print(f"Matched files: {result.matched_file_count} ({result.matched_bytes} bytes)")
        if result.cutoff_utc is not None:
            print(f"Cutoff: {result.cutoff_utc}")
        if result.active_session_output_path is not None:
            print(f"Excluded active session output: {result.active_session_output_path}")
        print(
            f"Empty directories {'removed' if result.write else 'matched'}: "
            f"{result.matched_directory_count}"
        )
        if result.matched_file_paths:
            print("Matched files:")
            for path in result.matched_file_paths:
                print(f"- {path}")
        if result.pruned_directory_paths:
            print(f"{'Removed' if result.write else 'Would remove'} empty directories:")
            for path in result.pruned_directory_paths:
                print(f"- {path}")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )
