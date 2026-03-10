"""Runtime handlers for validation command families."""

from __future__ import annotations

import argparse
from collections.abc import Callable

from watchtower_core.cli.handler_common import (
    _emit_command_error,
    _print_payload,
    _resolve_output_path,
)
from watchtower_core.control_plane.errors import SchemaResolutionError
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.evidence import EvidenceWriteResult, ValidationEvidenceRecorder
from watchtower_core.repo_ops.validation import VALIDATION_FAMILY_SPECS, ValidationAllService
from watchtower_core.validation import (
    AcceptanceReconciliationService,
    ArtifactValidationService,
    DocumentSemanticsValidationService,
    FrontMatterValidationService,
    ValidationExecutionError,
    ValidationResult,
    ValidationSelectionError,
)

ValidationServiceFactory = Callable[
    [ControlPlaneLoader],
    FrontMatterValidationService | DocumentSemanticsValidationService | ArtifactValidationService,
]


def _run_validate_front_matter(args: argparse.Namespace) -> int:
    return _run_validation_command(
        args,
        command_name="watchtower-core validate front-matter",
        success_message="Front matter validated successfully.",
        service_factory=FrontMatterValidationService,
    )


def _run_validate_document_semantics(args: argparse.Namespace) -> int:
    return _run_validation_command(
        args,
        command_name="watchtower-core validate document-semantics",
        success_message="Document semantics validated successfully.",
        service_factory=DocumentSemanticsValidationService,
    )


def _run_validate_artifact(args: argparse.Namespace) -> int:
    command_name = "watchtower-core validate artifact"
    message = _validate_evidence_arguments(args)
    if message is not None:
        return _emit_command_error(args, command_name, message)

    try:
        loader = ControlPlaneLoader(
            supplemental_schema_paths=tuple(args.supplemental_schema_path),
        )
    except SchemaResolutionError as exc:
        return _emit_command_error(args, command_name, str(exc), prefix="Validation error")

    service = ArtifactValidationService(loader)
    try:
        result = service.validate(
            args.path,
            validator_id=args.validator_id,
            schema_id=args.schema_id,
        )
    except (
        SchemaResolutionError,
        ValidationExecutionError,
        ValidationSelectionError,
    ) as exc:
        return _emit_command_error(args, command_name, str(exc), prefix="Validation error")

    evidence_write = None
    if args.record_evidence:
        recorder = ValidationEvidenceRecorder(loader)
        try:
            evidence_write = recorder.record(
                result,
                trace_id=args.trace_id,
                evidence_id=args.evidence_id,
                subject_ids=tuple(args.subject_id),
                acceptance_ids=tuple(args.acceptance_id),
                evidence_output=_resolve_output_path(args.evidence_output),
                traceability_output=_resolve_output_path(args.traceability_output),
            )
        except ValueError as exc:
            return _emit_command_error(args, command_name, str(exc), prefix="Validation error")

    result_payload = _build_validation_payload(
        command_name=command_name,
        result=result,
        evidence_write=evidence_write,
    )
    if _print_payload(args, result_payload) == 0:
        return 0 if result.passed else 1

    return _print_validation_summary(
        result,
        evidence_write=evidence_write,
        success_message="Artifact validated successfully.",
    )


def _run_validate_all(args: argparse.Namespace) -> int:
    service = ValidationAllService(ControlPlaneLoader())
    try:
        result = service.run(
            included_families=tuple(
                spec.family
                for spec in VALIDATION_FAMILY_SPECS
                if not getattr(args, spec.cli_skip_attr)
            ),
        )
    except ValueError as exc:
        return _emit_command_error(
            args,
            "watchtower-core validate all",
            str(exc),
            prefix="Validation error",
        )

    payload = {
        "command": "watchtower-core validate all",
        "status": "ok",
        "passed": result.passed,
        "total_count": result.total_count,
        "passed_count": result.passed_count,
        "failed_count": result.failed_count,
        "included_families": list(result.included_families),
        "family_summaries": [
            {
                "family": summary.family,
                "total_count": summary.total_count,
                "passed_count": summary.passed_count,
                "failed_count": summary.failed_count,
            }
            for summary in result.family_summaries
        ],
        "results": [
            {
                "family": record.family,
                "target": record.target,
                "validator_id": record.result.validator_id,
                "target_path": record.result.target_path,
                "engine": record.result.engine,
                "schema_ids": list(record.result.schema_ids),
                "passed": record.result.passed,
                "issue_count": record.issue_count,
                "issues": [
                    {
                        "code": issue.code,
                        "message": issue.message,
                        "location": issue.location,
                        "schema_id": issue.schema_id,
                    }
                    for issue in record.result.issues
                ],
            }
            for record in result.records
        ],
    }
    exit_code = 0 if result.passed else 1
    if _print_payload(args, payload) == 0:
        return exit_code

    print(
        "Ran validate all across "
        f"{result.total_count} targets: {result.passed_count} passed, "
        f"{result.failed_count} failed."
    )
    for summary in result.family_summaries:
        print(
            f"- {summary.family}: total={summary.total_count}, "
            f"passed={summary.passed_count}, failed={summary.failed_count}"
        )
    if result.failed_count:
        print("Failed targets:")
        for record in result.records:
            if record.result.passed:
                continue
            print(f"- {record.family}: {record.target}")
            if record.result.issues:
                print(f"  {record.result.issues[0].message}")
    return exit_code


def _run_validate_acceptance(args: argparse.Namespace) -> int:
    result = AcceptanceReconciliationService(ControlPlaneLoader()).validate(args.trace_id)
    payload = _build_validation_payload(
        command_name="watchtower-core validate acceptance",
        result=result,
        evidence_write=None,
    )
    exit_code = 0 if result.passed else 1
    if _print_payload(args, payload) == 0:
        return exit_code

    return _print_validation_summary(
        result,
        evidence_write=None,
        success_message="Acceptance reconciliation passed.",
    )


def _run_validation_command(
    args: argparse.Namespace,
    *,
    command_name: str,
    success_message: str,
    service_factory: ValidationServiceFactory,
) -> int:
    message = _validate_evidence_arguments(args)
    if message is not None:
        return _emit_command_error(args, command_name, message)

    loader = ControlPlaneLoader()
    service = service_factory(loader)
    try:
        result = service.validate(args.path, validator_id=args.validator_id)
    except (ValidationExecutionError, ValidationSelectionError) as exc:
        return _emit_command_error(args, command_name, str(exc), prefix="Validation error")

    evidence_write = None
    if args.record_evidence:
        recorder = ValidationEvidenceRecorder(loader)
        try:
            evidence_write = recorder.record(
                result,
                trace_id=args.trace_id,
                evidence_id=args.evidence_id,
                subject_ids=tuple(args.subject_id),
                acceptance_ids=tuple(args.acceptance_id),
                evidence_output=_resolve_output_path(args.evidence_output),
                traceability_output=_resolve_output_path(args.traceability_output),
            )
        except ValueError as exc:
            return _emit_command_error(args, command_name, str(exc), prefix="Validation error")

    result_payload = _build_validation_payload(
        command_name=command_name,
        result=result,
        evidence_write=evidence_write,
    )
    if _print_payload(args, result_payload) == 0:
        return 0 if result.passed else 1

    return _print_validation_summary(
        result,
        evidence_write=evidence_write,
        success_message=success_message,
    )


def _validate_evidence_arguments(args: argparse.Namespace) -> str | None:
    if not args.record_evidence and (
        args.trace_id
        or args.evidence_id
        or args.subject_id
        or args.acceptance_id
        or args.evidence_output is not None
        or args.traceability_output is not None
    ):
        return (
            "--trace-id, --evidence-id, --subject-id, --acceptance-id, "
            "--evidence-output, and --traceability-output require --record-evidence."
        )
    if args.record_evidence and not args.trace_id:
        return "--trace-id is required when --record-evidence is used."
    return None


def _build_validation_payload(
    *,
    command_name: str,
    result: ValidationResult,
    evidence_write: EvidenceWriteResult | None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "command": command_name,
        "status": "ok",
        "passed": result.passed,
        "validator_id": result.validator_id,
        "target_path": result.target_path,
        "engine": result.engine,
        "schema_ids": list(result.schema_ids),
        "issue_count": result.issue_count,
        "issues": [
            {
                "code": issue.code,
                "message": issue.message,
                "location": issue.location,
                "schema_id": issue.schema_id,
            }
            for issue in result.issues
        ],
    }
    if evidence_write is not None:
        payload["evidence"] = {
            "evidence_id": evidence_write.evidence_id,
            "evidence_relative_path": evidence_write.evidence_relative_path,
            "trace_id": evidence_write.trace_id,
            "recorded_at": evidence_write.recorded_at,
            "overall_result": evidence_write.overall_result,
            "evidence_output_path": evidence_write.evidence_output_path,
            "traceability_output_path": evidence_write.traceability_output_path,
        }
    return payload


def _print_validation_summary(
    result: ValidationResult,
    *,
    evidence_write: EvidenceWriteResult | None,
    success_message: str,
) -> int:
    verdict = "PASS" if result.passed else "FAIL"
    print(f"{verdict} {result.target_path}")
    print(f"Validator: {result.validator_id}")
    if result.schema_ids:
        print(f"Schemas: {', '.join(result.schema_ids)}")
    if evidence_write is not None:
        print(f"Evidence: {evidence_write.evidence_id}")
        print(f"Evidence Path: {evidence_write.evidence_output_path}")
        print(f"Traceability Path: {evidence_write.traceability_output_path}")
    if result.passed:
        print(success_message)
        return 0

    print(f"Issues: {result.issue_count}")
    for issue in result.issues:
        location = f" ({issue.location})" if issue.location else ""
        schema = f" [{issue.schema_id}]" if issue.schema_id else ""
        print(f"- {issue.code}{location}{schema}: {issue.message}")
    return 1
