"""Runtime handlers for validation command families."""

from __future__ import annotations

import argparse
from collections.abc import Callable

from watchtower_core.cli.handler_common import (
    _emit_command_error,
    _emit_detail_result,
    _resolve_output_path,
    _run_value_error_operation,
)
from watchtower_core.control_plane.errors import SchemaResolutionError
from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.evidence import EvidenceWriteResult, ValidationEvidenceRecorder
from watchtower_core.plan_runtime.validation import DocumentSemanticsValidationService
from watchtower_core.plan_runtime.validation.targets import (
    resolve_pack_validation_suite_targets,
)
from watchtower_core.validation import (
    AcceptanceReconciliationService,
    ArtifactValidationService,
    FrontMatterValidationService,
    ValidationExecutionError,
    ValidationResult,
    ValidationSelectionError,
    ValidationSuiteResult,
    ValidationSuiteService,
)
from watchtower_core.validation.all import VALIDATION_ALL_FAMILIES, ValidationAllService

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
            active_pack_settings_path=getattr(args, "pack_settings_path", None),
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
        evidence_write = _run_value_error_operation(
            args,
            command_name=command_name,
            prefix="Validation error",
            operation=lambda: recorder.record(
                result,
                trace_id=args.trace_id,
                evidence_id=args.evidence_id,
                subject_ids=tuple(args.subject_id),
                acceptance_ids=tuple(args.acceptance_id),
                evidence_output=_resolve_output_path(args.evidence_output),
                traceability_output=_resolve_output_path(args.traceability_output),
            ),
        )
        if evidence_write is None:
            return 1

    result_payload = _build_validation_payload(
        command_name=command_name,
        result=result,
        evidence_write=evidence_write,
    )
    return _emit_detail_result(
        args,
        payload_factory=lambda: result_payload,
        render_human=lambda: _print_validation_summary(
            result,
            evidence_write=evidence_write,
            success_message="Artifact validated successfully.",
        ),
        exit_code=0 if result.passed else 1,
    )


def _run_validate_suite(args: argparse.Namespace) -> int:
    pack_settings_path = getattr(args, "pack_settings_path", None) or PACK_SETTINGS_PATH
    loader = ControlPlaneLoader(
        active_pack_settings_path=getattr(args, "pack_settings_path", None)
    )
    service = ValidationSuiteService(
        loader,
        target_resolver=resolve_pack_validation_suite_targets,
    )
    try:
        result = service.run(
            args.suite_id,
            pack_settings_path=pack_settings_path,
        )
    except (SchemaResolutionError, ValidationExecutionError, ValidationSelectionError) as exc:
        return _emit_command_error(
            args,
            "watchtower-core validate suite",
            str(exc),
            prefix="Validation error",
        )

    payload = _build_suite_validation_payload(result)
    exit_code = 0 if result.passed else 1
    def _render_human() -> None:
        print(
            "Ran validation suite "
            f"{result.suite_id} across {result.total_count} targets: "
            f"{result.passed_count} passed, {result.failed_count} failed."
        )
        for summary in result.step_summaries:
            print(
                f"- {summary.step_id} ({summary.step_kind}): total={summary.total_count}, "
                f"passed={summary.passed_count}, failed={summary.failed_count}"
            )
        if result.failed_count:
            print("Failed targets:")
            for record in result.records:
                if record.result.passed:
                    continue
                print(f"- {record.step_id}: {record.target}")
                if record.result.issues:
                    print(f"  {record.result.issues[0].message}")

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
        exit_code=exit_code,
    )


def _run_validate_all(args: argparse.Namespace) -> int:
    pack_settings_path = getattr(args, "pack_settings_path", None) or PACK_SETTINGS_PATH
    loader = ControlPlaneLoader(active_pack_settings_path=getattr(args, "pack_settings_path", None))
    suite_id = loader.load_pack_settings(pack_settings_path).default_validation_suite_id
    included_families = tuple(
        family
        for family in VALIDATION_ALL_FAMILIES
        if not getattr(
            args,
            {
                "front_matter": "skip_front_matter",
                "document_semantics": "skip_document_semantics",
                "artifacts": "skip_artifacts",
                "acceptance": "skip_acceptance",
            }[family],
        )
    )
    service = ValidationAllService(
        loader,
        suite_id=suite_id,
        pack_settings_path=pack_settings_path,
        suite_target_resolver=resolve_pack_validation_suite_targets,
    )
    result = _run_value_error_operation(
        args,
        command_name="watchtower-core validate all",
        prefix="Validation error",
        operation=lambda: service.run(included_families=included_families),
    )
    if result is None:
        return 1

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
    def _render_human() -> None:
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

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
        exit_code=exit_code,
    )


def _run_validate_acceptance(args: argparse.Namespace) -> int:
    result = AcceptanceReconciliationService(ControlPlaneLoader()).validate(args.trace_id)
    payload = _build_validation_payload(
        command_name="watchtower-core validate acceptance",
        result=result,
        evidence_write=None,
    )
    exit_code = 0 if result.passed else 1
    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=lambda: _print_validation_summary(
            result,
            evidence_write=None,
            success_message="Acceptance reconciliation passed.",
        ),
        exit_code=exit_code,
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

    loader = ControlPlaneLoader(active_pack_settings_path=getattr(args, "pack_settings_path", None))
    service = service_factory(loader)
    try:
        result = service.validate(args.path, validator_id=args.validator_id)
    except (ValidationExecutionError, ValidationSelectionError) as exc:
        return _emit_command_error(args, command_name, str(exc), prefix="Validation error")

    evidence_write = None
    if args.record_evidence:
        recorder = ValidationEvidenceRecorder(loader)
        evidence_write = _run_value_error_operation(
            args,
            command_name=command_name,
            prefix="Validation error",
            operation=lambda: recorder.record(
                result,
                trace_id=args.trace_id,
                evidence_id=args.evidence_id,
                subject_ids=tuple(args.subject_id),
                acceptance_ids=tuple(args.acceptance_id),
                evidence_output=_resolve_output_path(args.evidence_output),
                traceability_output=_resolve_output_path(args.traceability_output),
            ),
        )
        if evidence_write is None:
            return 1

    result_payload = _build_validation_payload(
        command_name=command_name,
        result=result,
        evidence_write=evidence_write,
    )
    return _emit_detail_result(
        args,
        payload_factory=lambda: result_payload,
        render_human=lambda: _print_validation_summary(
            result,
            evidence_write=evidence_write,
            success_message=success_message,
        ),
        exit_code=0 if result.passed else 1,
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


def _build_suite_validation_payload(result: ValidationSuiteResult) -> dict[str, object]:
    return {
        "command": "watchtower-core validate suite",
        "status": "ok",
        "suite_id": result.suite_id,
        "pack_settings_path": result.pack_settings_path,
        "passed": result.passed,
        "total_count": result.total_count,
        "passed_count": result.passed_count,
        "failed_count": result.failed_count,
        "step_summaries": [
            {
                "step_id": summary.step_id,
                "step_kind": summary.step_kind,
                "total_count": summary.total_count,
                "passed_count": summary.passed_count,
                "failed_count": summary.failed_count,
            }
            for summary in result.step_summaries
        ],
        "records": [
            {
                "step_id": record.step_id,
                "step_kind": record.step_kind,
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
