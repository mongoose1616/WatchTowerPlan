"""Public models for the plan workspace service."""

from __future__ import annotations

from dataclasses import dataclass


def _string_tuple(value: object) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,) if value else ()
    if not isinstance(value, (list, tuple)):
        return ()
    return tuple(item for item in value if isinstance(item, str) and item)


def _required_int(value: object) -> int:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    return int(str(value))


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str) and value:
        return int(value)
    return None


@dataclass(frozen=True, slots=True)
class PlanTaskIndexEntry:
    """Machine-readable task-summary entry for the plan workspace."""

    task_id: str
    initiative_id: str
    project_id: str | None
    trace_id: str
    initiative_title: str
    title: str
    summary: str
    status: str
    task_status: str
    task_kind: str
    priority: str
    owner: str
    doc_path: str
    updated_at: str
    blocked_by: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    related_ids: tuple[str, ...] = ()
    applies_to: tuple[str, ...] = ()
    github_repository: str | None = None
    github_issue_number: int | None = None
    github_issue_node_id: str | None = None
    github_project_owner: str | None = None
    github_project_owner_type: str | None = None
    github_project_number: int | None = None
    github_project_item_id: str | None = None
    github_synced_at: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, object]) -> PlanTaskIndexEntry:
        return cls(
            task_id=str(document["task_id"]),
            initiative_id=str(document["initiative_id"]),
            project_id=(
                str(document["project_id"])
                if document.get("project_id") is not None
                else None
            ),
            trace_id=str(document["trace_id"]),
            initiative_title=str(document["initiative_title"]),
            title=str(document["title"]),
            summary=str(document["summary"]),
            status=str(document["status"]),
            task_status=str(document["task_status"]),
            task_kind=str(document.get("task_kind", "feature")),
            priority=str(document["priority"]),
            owner=str(document["owner"]),
            doc_path=str(document["doc_path"]),
            updated_at=str(document["updated_at"]),
            blocked_by=_string_tuple(document.get("blocked_by")),
            depends_on=_string_tuple(document.get("depends_on")),
            related_ids=_string_tuple(document.get("related_ids")),
            applies_to=_string_tuple(document.get("applies_to")),
            github_repository=(
                str(document["github_repository"])
                if document.get("github_repository") is not None
                else None
            ),
            github_issue_number=_optional_int(document.get("github_issue_number")),
            github_issue_node_id=(
                str(document["github_issue_node_id"])
                if document.get("github_issue_node_id") is not None
                else None
            ),
            github_project_owner=(
                str(document["github_project_owner"])
                if document.get("github_project_owner") is not None
                else None
            ),
            github_project_owner_type=(
                str(document["github_project_owner_type"])
                if document.get("github_project_owner_type") is not None
                else None
            ),
            github_project_number=_optional_int(document.get("github_project_number")),
            github_project_item_id=(
                str(document["github_project_item_id"])
                if document.get("github_project_item_id") is not None
                else None
            ),
            github_synced_at=(
                str(document["github_synced_at"])
                if document.get("github_synced_at") is not None
                else None
            ),
        )


@dataclass(frozen=True, slots=True)
class PlanReadinessIndexEntry:
    """Machine-readable readiness-gate summary for one initiative package."""

    initiative_id: str
    project_id: str | None
    trace_id: str
    title: str
    initiative_root: str
    lifecycle_stage: str
    review_status: str
    capture_complete: bool
    machine_valid: bool
    approval_status: str
    ready_for_execution: bool
    blocking_reasons: tuple[str, ...]
    updated_at: str
    scope_type: str = "pack_wide"

    @classmethod
    def from_document(cls, document: dict[str, object]) -> PlanReadinessIndexEntry:
        return cls(
            initiative_id=str(document["initiative_id"]),
            project_id=(
                str(document["project_id"])
                if document.get("project_id") is not None
                else None
            ),
            trace_id=str(document["trace_id"]),
            title=str(document["title"]),
            initiative_root=str(document["initiative_root"]),
            lifecycle_stage=str(document["lifecycle_stage"]),
            review_status=str(document["review_status"]),
            capture_complete=bool(document["capture_complete"]),
            machine_valid=bool(document["machine_valid"]),
            approval_status=str(document["approval_status"]),
            ready_for_execution=bool(document["ready_for_execution"]),
            blocking_reasons=_string_tuple(document.get("blocking_reasons")),
            updated_at=str(document["updated_at"]),
            scope_type=str(document.get("scope_type", "pack_wide")),
        )


@dataclass(frozen=True, slots=True)
class PlanDiscrepancyIndexEntry:
    """Machine-readable discrepancy summary for one initiative-local discrepancy."""

    discrepancy_id: str
    initiative_id: str
    project_id: str | None
    trace_id: str
    title: str
    category: str
    severity: str
    gate_effect: str
    status: str
    summary: str
    source_paths: tuple[str, ...]
    updated_at: str

    @classmethod
    def from_document(cls, document: dict[str, object]) -> PlanDiscrepancyIndexEntry:
        return cls(
            discrepancy_id=str(document["discrepancy_id"]),
            initiative_id=str(document["initiative_id"]),
            project_id=(
                str(document["project_id"])
                if document.get("project_id") is not None
                else None
            ),
            trace_id=str(document["trace_id"]),
            title=str(document["title"]),
            category=str(document["category"]),
            severity=str(document["severity"]),
            gate_effect=str(document["gate_effect"]),
            status=str(document["status"]),
            summary=str(document["summary"]),
            source_paths=_string_tuple(document.get("source_paths")),
            updated_at=str(document["updated_at"]),
        )


@dataclass(frozen=True, slots=True)
class PlanEvidenceIndexEntry:
    """Machine-readable evidence summary entry for one initiative-local validation bundle."""

    evidence_id: str
    initiative_id: str
    project_id: str | None
    trace_id: str
    initiative_title: str
    title: str
    status: str
    initiative_root: str
    entry_count: int
    acceptance_labels: tuple[str, ...]
    validation_types: tuple[str, ...]
    owners: tuple[str, ...]
    target_phases: tuple[str, ...]
    expected_output_paths: tuple[str, ...]
    updated_at: str

    @classmethod
    def from_document(cls, document: dict[str, object]) -> PlanEvidenceIndexEntry:
        return cls(
            evidence_id=str(document["evidence_id"]),
            initiative_id=str(document["initiative_id"]),
            project_id=(
                str(document["project_id"])
                if document.get("project_id") is not None
                else None
            ),
            trace_id=str(document["trace_id"]),
            initiative_title=str(document["initiative_title"]),
            title=str(document["title"]),
            status=str(document["status"]),
            initiative_root=str(document["initiative_root"]),
            entry_count=_required_int(document["entry_count"]),
            acceptance_labels=_string_tuple(document.get("acceptance_labels")),
            validation_types=_string_tuple(document.get("validation_types")),
            owners=_string_tuple(document.get("owners")),
            target_phases=_string_tuple(document.get("target_phases")),
            expected_output_paths=_string_tuple(document.get("expected_output_paths")),
            updated_at=str(document["updated_at"]),
        )


@dataclass(frozen=True, slots=True)
class PlanCloseoutIndexEntry:
    """Machine-readable closeout summary entry for one initiative-local closeout recap."""

    closeout_id: str
    initiative_id: str
    project_id: str | None
    trace_id: str
    initiative_title: str
    title: str
    status: str
    initiative_root: str
    expected_outcome: str
    acceptance_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    follow_up_handling: str
    promotion_review_required: bool
    terminal_state_options: tuple[str, ...]
    terminal_state: str | None
    updated_at: str

    @classmethod
    def from_document(cls, document: dict[str, object]) -> PlanCloseoutIndexEntry:
        return cls(
            closeout_id=str(document["closeout_id"]),
            initiative_id=str(document["initiative_id"]),
            project_id=(
                str(document["project_id"])
                if document.get("project_id") is not None
                else None
            ),
            trace_id=str(document["trace_id"]),
            initiative_title=str(document["initiative_title"]),
            title=str(document["title"]),
            status=str(document["status"]),
            initiative_root=str(document["initiative_root"]),
            expected_outcome=str(document["expected_outcome"]),
            acceptance_ids=_string_tuple(document.get("acceptance_ids")),
            evidence_ids=_string_tuple(document.get("evidence_ids")),
            follow_up_handling=str(document["follow_up_handling"]),
            promotion_review_required=bool(document["promotion_review_required"]),
            terminal_state_options=_string_tuple(document.get("terminal_state_options")),
            terminal_state=(
                str(document["terminal_state"])
                if document.get("terminal_state") is not None
                else None
            ),
            updated_at=str(document["updated_at"]),
        )


@dataclass(frozen=True, slots=True)
class PlanReviewIndexEntry:
    """Machine-readable review summary entry for live initiative and promotion review state."""

    review_subject_id: str
    subject_kind: str
    initiative_id: str
    project_id: str | None
    trace_id: str
    initiative_title: str
    title: str
    review_state: str
    review_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    updated_at: str
    lifecycle_stage: str | None = None
    ready_for_execution: bool | None = None

    @classmethod
    def from_document(cls, document: dict[str, object]) -> PlanReviewIndexEntry:
        return cls(
            review_subject_id=str(document["review_subject_id"]),
            subject_kind=str(document["subject_kind"]),
            initiative_id=str(document["initiative_id"]),
            project_id=(
                str(document["project_id"])
                if document.get("project_id") is not None
                else None
            ),
            trace_id=str(document["trace_id"]),
            initiative_title=str(document["initiative_title"]),
            title=str(document["title"]),
            review_state=str(document["review_state"]),
            review_refs=_string_tuple(document.get("review_refs")),
            evidence_refs=_string_tuple(document.get("evidence_refs")),
            updated_at=str(document["updated_at"]),
            lifecycle_stage=(
                str(document["lifecycle_stage"])
                if document.get("lifecycle_stage") is not None
                else None
            ),
            ready_for_execution=(
                bool(document["ready_for_execution"])
                if document.get("ready_for_execution") is not None
                else None
            ),
        )


@dataclass(frozen=True, slots=True)
class PlanPromotionIndexEntry:
    """Machine-readable promotion-summary entry for one initiative-local record."""

    promotion_id: str
    initiative_id: str
    project_id: str | None
    trace_id: str
    initiative_title: str
    title: str
    status: str
    initiative_root: str
    candidate_count: int
    candidate_paths: tuple[str, ...]
    target_paths: tuple[str, ...]
    target_families: tuple[str, ...]
    review_paths: tuple[str, ...]
    updated_at: str
    approval_state: str | None = None
    evidence_refs: tuple[str, ...] = ()
    provenance_expectations: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, object]) -> PlanPromotionIndexEntry:
        return cls(
            promotion_id=str(document["promotion_id"]),
            initiative_id=str(document["initiative_id"]),
            project_id=(
                str(document["project_id"])
                if document.get("project_id") is not None
                else None
            ),
            trace_id=str(document["trace_id"]),
            initiative_title=str(document["initiative_title"]),
            title=str(document["title"]),
            status=str(document["status"]),
            initiative_root=str(document["initiative_root"]),
            candidate_count=_required_int(document["candidate_count"]),
            candidate_paths=_string_tuple(document.get("candidate_paths")),
            target_paths=_string_tuple(document.get("target_paths")),
            target_families=_string_tuple(document.get("target_families")),
            review_paths=_string_tuple(document.get("review_paths")),
            updated_at=str(document["updated_at"]),
            approval_state=(
                str(document["approval_state"])
                if document.get("approval_state") is not None
                else None
            ),
            evidence_refs=_string_tuple(document.get("evidence_refs")),
            provenance_expectations=_string_tuple(
                document.get("provenance_expectations")
            ),
        )


@dataclass(frozen=True, slots=True)
class PlanGuidanceIndexEntry:
    """Machine-readable plan-guidance summary entry for one promoted document."""

    guidance_id: str
    title: str
    summary: str
    guidance_family: str
    status: str
    owner: str
    doc_path: str
    updated_at: str
    trace_id: str | None = None
    audience: str | None = None
    authority: str | None = None
    tags: tuple[str, ...] = ()
    applies_to: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, object]) -> PlanGuidanceIndexEntry:
        return cls(
            guidance_id=str(document["guidance_id"]),
            title=str(document["title"]),
            summary=str(document["summary"]),
            guidance_family=str(document["guidance_family"]),
            status=str(document["status"]),
            owner=str(document["owner"]),
            doc_path=str(document["doc_path"]),
            updated_at=str(document["updated_at"]),
            trace_id=(
                str(document["trace_id"])
                if document.get("trace_id") is not None
                else None
            ),
            audience=(
                str(document["audience"])
                if document.get("audience") is not None
                else None
            ),
            authority=(
                str(document["authority"])
                if document.get("authority") is not None
                else None
            ),
            tags=_string_tuple(document.get("tags")),
            applies_to=_string_tuple(document.get("applies_to")),
        )


@dataclass(frozen=True, slots=True)
class PlanTaskSearchParams:
    """Structured task lookup filters for plan-workspace task summaries."""

    query: str | None = None
    initiative_id: str | None = None
    project_id: str | None = None
    trace_id: str | None = None
    status: str | None = None
    priority: str | None = None
    owner: str | None = None
    blocked_only: bool = False
    limit: int | None = None


@dataclass(frozen=True, slots=True)
class PlanReadinessSearchParams:
    """Structured readiness lookup filters for initiative packages."""

    query: str | None = None
    initiative_id: str | None = None
    project_id: str | None = None
    trace_id: str | None = None
    lifecycle_stage: str | None = None
    review_status: str | None = None
    ready_for_execution: bool | None = None
    blocked_only: bool = False
    limit: int | None = None


@dataclass(frozen=True, slots=True)
class PlanDiscrepancySearchParams:
    """Structured discrepancy lookup filters for plan-workspace discrepancies."""

    query: str | None = None
    initiative_id: str | None = None
    project_id: str | None = None
    trace_id: str | None = None
    category: str | None = None
    severity: str | None = None
    status: str | None = None
    blocking_only: bool = False
    limit: int | None = None


@dataclass(frozen=True, slots=True)
class PlanEvidenceSearchParams:
    """Structured evidence lookup filters for live initiative-local validation bundles."""

    query: str | None = None
    initiative_id: str | None = None
    project_id: str | None = None
    trace_id: str | None = None
    status: str | None = None
    owner: str | None = None
    target_phase: str | None = None
    validation_type: str | None = None
    acceptance_label: str | None = None
    limit: int | None = None


@dataclass(frozen=True, slots=True)
class PlanCloseoutSearchParams:
    """Structured closeout lookup filters for live initiative-local closeout recaps."""

    query: str | None = None
    initiative_id: str | None = None
    project_id: str | None = None
    trace_id: str | None = None
    status: str | None = None
    terminal_state: str | None = None
    promotion_review_required: bool | None = None
    limit: int | None = None


@dataclass(frozen=True, slots=True)
class PlanReviewSearchParams:
    """Structured review lookup filters for live initiative and promotion review state."""

    query: str | None = None
    subject_kind: str | None = None
    initiative_id: str | None = None
    project_id: str | None = None
    trace_id: str | None = None
    review_state: str | None = None
    ready_for_execution: bool | None = None
    review_ref: str | None = None
    limit: int | None = None


@dataclass(frozen=True, slots=True)
class PlanWorkspaceSyncResult:
    """Summary of one plan-workspace rebuild run."""

    initiative_count: int
    task_count: int
    discrepancy_count: int
    wrote: bool
