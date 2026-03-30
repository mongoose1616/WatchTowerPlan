"""Runtime handlers for planning-record query commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import (
    _emit_collection_query_results,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    AcceptanceContract,
    BenchmarkRecordArtifact,
    ValidationEvidenceArtifact,
)
from watchtower_core.query import (
    AcceptanceContractQueryService,
    AcceptanceContractSearchParams,
    BenchmarkRecordQueryService,
    BenchmarkRecordSearchParams,
    ValidationEvidenceQueryService,
    ValidationEvidenceSearchParams,
)


def _run_query_acceptance(args: argparse.Namespace) -> int:
    service = AcceptanceContractQueryService(ControlPlaneLoader())
    entries = service.search(
        AcceptanceContractSearchParams(
            trace_id=args.trace_id,
            source_surface_path=args.source_surface_path,
            acceptance_id=args.acceptance_id,
        )
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query acceptance",
        entries=entries,
        noun="acceptance contract",
        empty_message="No acceptance contracts matched the requested filters.",
        payload_results_factory=lambda: [
            _acceptance_contract_entry_payload(entry) for entry in entries
        ],
        render_entry=_print_acceptance_contract_entry,
    )


def _run_query_evidence(args: argparse.Namespace) -> int:
    service = ValidationEvidenceQueryService(ControlPlaneLoader())
    entries = service.search(
        ValidationEvidenceSearchParams(
            trace_id=args.trace_id,
            overall_result=args.result,
            acceptance_id=args.acceptance_id,
            validator_id=args.validator_id,
        )
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query evidence",
        entries=entries,
        noun="validation-evidence artifact",
        empty_message="No validation-evidence artifacts matched the requested filters.",
        payload_results_factory=lambda: [_evidence_entry_payload(entry) for entry in entries],
        render_entry=_print_evidence_entry,
    )


def _run_query_benchmarks(args: argparse.Namespace) -> int:
    service = BenchmarkRecordQueryService(ControlPlaneLoader())
    entries = service.search(
        BenchmarkRecordSearchParams(
            record_id=args.record_id,
            suite_id=args.suite_id,
            limit=args.limit,
        )
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query benchmarks",
        entries=entries,
        noun="benchmark record",
        empty_message="No benchmark records matched the requested filters.",
        payload_results_factory=lambda: [_benchmark_entry_payload(entry) for entry in entries],
        render_entry=_print_benchmark_entry,
    )


def _acceptance_contract_entry_payload(entry: AcceptanceContract) -> dict[str, object]:
    return {
        "contract_id": entry.contract_id,
        "title": entry.title,
        "status": entry.status,
        "trace_id": entry.trace_id,
        "source_surface_path": entry.source_surface_path,
        "doc_path": entry.doc_path,
        "acceptance_ids": [item.acceptance_id for item in entry.entries],
        "required_validator_ids": sorted(
            {
                validator_id
                for item in entry.entries
                for validator_id in item.required_validator_ids
            }
        ),
    }


def _print_acceptance_contract_entry(entry: AcceptanceContract) -> None:
    print(f"- {entry.contract_id} [{entry.status}]")
    print(f"  Trace: {entry.trace_id}")
    print(f"  Source Surface: {entry.source_surface_path}")
    print(f"  Acceptance IDs: {', '.join(item.acceptance_id for item in entry.entries)}")


def _evidence_entry_payload(entry: ValidationEvidenceArtifact) -> dict[str, object]:
    return {
        "evidence_id": entry.evidence_id,
        "title": entry.title,
        "status": entry.status,
        "trace_id": entry.trace_id,
        "overall_result": entry.overall_result,
        "recorded_at": entry.recorded_at,
        "doc_path": entry.doc_path,
        "source_surface_paths": list(entry.source_surface_paths),
        "source_acceptance_contract_ids": list(entry.source_acceptance_contract_ids),
        "check_count": len(entry.checks),
        "acceptance_ids": sorted(
            {
                acceptance_id
                for check in entry.checks
                for acceptance_id in check.acceptance_ids
            }
        ),
    }


def _print_evidence_entry(entry: ValidationEvidenceArtifact) -> None:
    print(f"- {entry.evidence_id} [{entry.overall_result}]")
    print(f"  Trace: {entry.trace_id}")
    print(f"  Recorded At: {entry.recorded_at}")
    print(f"  Checks: {len(entry.checks)}")


def _benchmark_entry_payload(entry: BenchmarkRecordArtifact) -> dict[str, object]:
    return {
        "record_id": entry.record_id,
        "title": entry.title,
        "status": entry.status,
        "benchmark_kind": entry.benchmark_kind,
        "suite_id": entry.suite_id,
        "suite_title": entry.suite_title,
        "recorded_at": entry.recorded_at,
        "doc_path": entry.doc_path,
        "command_count": len(entry.commands),
        "baseline_record_path": entry.baseline_record_path,
    }


def _print_benchmark_entry(entry: BenchmarkRecordArtifact) -> None:
    print(f"- {entry.record_id} [{entry.benchmark_kind}]")
    print(f"  Suite: {entry.suite_id}")
    print(f"  Recorded At: {entry.recorded_at}")
    print(f"  Commands: {len(entry.commands)}")
