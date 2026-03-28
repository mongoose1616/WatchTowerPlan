"""Plan-workspace orchestration façade over workspace loaders, builders, and search helpers."""

from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane import DiscrepancyIssue
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    CoordinationIndex,
    InitiativeIndex,
    InitiativeIndexEntry,
)
from watchtower_core.control_plane.pack_workspace import PackWorkspacePaths
from watchtower_core.control_plane.terminology import TerminologyHelper
from watchtower_core.evidence import EvidenceBundleHelper
from watchtower_core.query.rendered_search import (
    RenderedSearchFilters,
    initiative_rendered_query_terms,
    search_rendered_entries,
)
from watchtower_core.rebuild import (
    MarkdownReconciliationHelper,
    RebuildHarness,
    RebuildOutput,
    RebuildTargetSpec,
    RenderedViewBuilder,
)
from watchtower_plan.workspace.artifacts import (
    PLAN_ARTIFACT_INDEX_PATH,
    ArtifactIndexService,
)
from watchtower_plan.workspace.builders import PlanWorkspaceDocumentBuilder
from watchtower_plan.workspace.constants import (
    INITIATIVE_PLAN_SURFACE_ID,
    INITIATIVE_PROGRESS_SURFACE_ID,
    INITIATIVE_SUMMARY_SURFACE_ID,
    PHASE_ORDER,
    PLAN_CLOSEOUT_INDEX_PATH,
    PLAN_COORDINATION_INDEX_PATH,
    PLAN_DISCREPANCY_INDEX_PATH,
    PLAN_EVIDENCE_INDEX_PATH,
    PLAN_GUIDANCE_INDEX_PATH,
    PLAN_INITIATIVE_INDEX_PATH,
    PLAN_OVERVIEW_PATH,
    PLAN_OVERVIEW_SURFACE_ID,
    PLAN_PACK_SETTINGS_PATH,
    PLAN_PROMOTION_INDEX_PATH,
    PLAN_READINESS_INDEX_PATH,
    PLAN_REVIEW_INDEX_PATH,
    PLAN_TASK_INDEX_PATH,
)
from watchtower_plan.workspace.models import (
    PlanCloseoutIndexEntry,
    PlanCloseoutSearchParams,
    PlanDiscrepancyIndexEntry,
    PlanDiscrepancySearchParams,
    PlanEvidenceIndexEntry,
    PlanEvidenceSearchParams,
    PlanGuidanceIndexEntry,
    PlanPromotionIndexEntry,
    PlanReadinessIndexEntry,
    PlanReadinessSearchParams,
    PlanReviewIndexEntry,
    PlanReviewSearchParams,
    PlanTaskIndexEntry,
    PlanTaskSearchParams,
    PlanWorkspaceSyncResult,
)
from watchtower_plan.workspace.rendering import PlanWorkspaceRenderer
from watchtower_plan.workspace.search import (
    search_closeout_entries,
    search_discrepancy_entries,
    search_evidence_entries,
    search_readiness_entries,
    search_review_entries,
    search_task_entries,
)
from watchtower_plan.workspace.snapshots import PlanWorkspaceSnapshotLoader
from watchtower_plan.workspace.support import json_document, plan_markdown_issue_summary


class PlanWorkspaceService:
    """Build plan-local indexes, rendered views, and query surfaces."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._pack_loader = loader.derive(active_pack_settings_path=PLAN_PACK_SETTINGS_PATH)
        self._workspace_paths = PackWorkspacePaths.from_loader(
            self._pack_loader,
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
        self._initiative_index_path = self._workspace_paths.index_path(
            "initiative_index.json"
        )
        self._task_index_path = self._workspace_paths.index_path("task_index.json")
        self._readiness_index_path = self._workspace_paths.index_path(
            "readiness_index.json"
        )
        self._discrepancy_index_path = self._workspace_paths.index_path(
            "discrepancy_index.json"
        )
        self._evidence_index_path = self._workspace_paths.index_path(
            "evidence_index.json"
        )
        self._closeout_index_path = self._workspace_paths.index_path(
            "closeout_index.json"
        )
        self._review_index_path = self._workspace_paths.index_path("review_index.json")
        self._promotion_index_path = self._workspace_paths.index_path(
            "promotion_index.json"
        )
        self._guidance_index_path = self._workspace_paths.index_path(
            "guidance_index.json"
        )
        self._coordination_index_path = self._workspace_paths.index_path(
            "coordination_index.json"
        )
        self._artifact_index_path = self._workspace_paths.index_path(
            "artifact_index.json"
        )
        self._overview_path = self._workspace_paths.overview_path
        self._snapshot_loader = PlanWorkspaceSnapshotLoader(loader, self._workspace_paths)
        self._vocabulary: TerminologyHelper | None = None
        self._renderer: PlanWorkspaceRenderer | None = None
        self._builder: PlanWorkspaceDocumentBuilder | None = None
        self._markdown_reconciliation: MarkdownReconciliationHelper | None = None

    def sync(self, *, write: bool) -> PlanWorkspaceSyncResult:
        snapshots = self._snapshot_loader.load_initiative_snapshots()
        builder = self._builder_service()
        documents = builder.build_documents(snapshots)
        artifact_document = ArtifactIndexService(self._loader).build_document(
            aggregate_overrides=builder.artifact_aggregate_overrides(documents)
        )
        rebuild_outputs = builder.build_rebuild_outputs(documents, artifact_document)
        rebuild_result = RebuildHarness(self._loader).run_specs(
            (
                RebuildTargetSpec(
                    target="plan-workspace",
                    build_outputs=lambda _loader: rebuild_outputs,
                ),
            ),
            write=write,
        )
        if write:
            self._refresh_pack_runtime_state()
        task_index_entries = self._entries(self._json_document(documents["task_index"]))
        discrepancy_index_entries = self._entries(
            self._json_document(documents["discrepancy_index"])
        )
        return PlanWorkspaceSyncResult(
            initiative_count=len(snapshots),
            task_count=len(task_index_entries),
            discrepancy_count=len(discrepancy_index_entries),
            wrote=rebuild_result.wrote,
        )

    def sync_discrepancy_index(self, *, write: bool) -> bool:
        """Rebuild only the discrepancy index without healing unrelated derived surfaces."""

        snapshots = self._snapshot_loader.load_initiative_snapshots()
        documents = self._builder_service().build_documents(snapshots)
        rebuild_result = RebuildHarness(self._loader).run_specs(
            (
                RebuildTargetSpec(
                    target="plan-workspace-discrepancy-index",
                    build_outputs=lambda _loader: (
                        RebuildOutput(
                            relative_output_path=self._discrepancy_index_path,
                            artifact_kind="index",
                            output_format="json",
                            content=json_document(documents["discrepancy_index"]),
                            validated=True,
                        ),
                    ),
                ),
            ),
            write=write,
        )
        if write:
            self._refresh_pack_runtime_state()
        return rebuild_result.wrote

    def expected_surface_issues(
        self, initiative_root: str
    ) -> tuple[DiscrepancyIssue, ...]:
        snapshots = self._snapshot_loader.load_initiative_snapshots()
        documents = self._builder_service().build_documents(snapshots)
        snapshot = next(
            (
                candidate
                for candidate in snapshots
                if candidate.initiative_root == initiative_root
            ),
            None,
        )
        discrepancy_namespace = (
            snapshot.discrepancy_namespace
            if snapshot is not None
            else Path(initiative_root).name
        )
        initiative_views = documents["initiative_views"]
        assert isinstance(initiative_views, dict)
        expected_markdown = {
            self._overview_path: str(documents["plan_overview"]),
            f"{initiative_root}/plan.md": str(
                initiative_views.get(f"{initiative_root}/plan.md", "")
            ),
            f"{initiative_root}/progress.md": str(
                initiative_views.get(f"{initiative_root}/progress.md", "")
            ),
            f"{initiative_root}/summary.md": str(
                initiative_views.get(f"{initiative_root}/summary.md", "")
            ),
        }
        artifact_document = ArtifactIndexService(self._loader).build_document(
            aggregate_overrides=self._builder_service().artifact_aggregate_overrides(
                documents
            )
        )
        expected_json = {
            **self._builder_service().artifact_aggregate_overrides(documents),
            self._artifact_index_path: artifact_document,
        }

        issues: list[DiscrepancyIssue] = []
        for issue in self._markdown_reconciliation_service().expected_issues(
            expected_markdown
        ):
            relative_path = issue.relative_output_path
            issues.append(
                DiscrepancyIssue(
                    record_slug=f"{Path(relative_path).stem}_surface_drift",
                    category="stale_rendered_surface",
                    summary=plan_markdown_issue_summary(
                        issue.issue_code,
                        relative_path,
                    ),
                    source_paths=(relative_path,),
                    discrepancy_id=(
                        f"discrepancy.{discrepancy_namespace}.{Path(relative_path).stem}_surface_drift"
                    ),
                )
            )

        for relative_path, expected in expected_json.items():
            candidate = self._loader.repo_root / relative_path
            if not candidate.exists():
                issues.append(
                    DiscrepancyIssue(
                        record_slug=f"{Path(relative_path).stem}_index_drift",
                        category="stale_aggregate_index",
                        summary=f"Required aggregate index is missing: {relative_path}.",
                        source_paths=(relative_path,),
                        discrepancy_id=(
                            f"discrepancy.{discrepancy_namespace}.{Path(relative_path).stem}_index_drift"
                        ),
                    )
                )
                continue
            try:
                current = json.loads(candidate.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                issues.append(
                    DiscrepancyIssue(
                        record_slug=f"{Path(relative_path).stem}_index_drift",
                        category="stale_aggregate_index",
                        summary=f"Aggregate index is not valid JSON: {relative_path}.",
                        source_paths=(relative_path,),
                        discrepancy_id=(
                            f"discrepancy.{discrepancy_namespace}.{Path(relative_path).stem}_index_drift"
                        ),
                    )
                )
                continue
            if current != expected:
                issues.append(
                    DiscrepancyIssue(
                        record_slug=f"{Path(relative_path).stem}_index_drift",
                        category="stale_aggregate_index",
                        summary=f"Aggregate index drift detected for {relative_path}.",
                        source_paths=(relative_path,),
                        discrepancy_id=(
                            f"discrepancy.{discrepancy_namespace}.{Path(relative_path).stem}_index_drift"
                        ),
                    )
                )
        return tuple(
            sorted(
                issues,
                key=lambda issue: (issue.category, issue.source_paths[0]),
            )
        )

    def load_initiative_index(self) -> InitiativeIndex:
        return InitiativeIndex.from_document(
            self._load_plan_json(self._initiative_index_path)
        )

    def load_coordination_index(self) -> CoordinationIndex:
        return CoordinationIndex.from_document(
            self._load_plan_json(self._coordination_index_path)
        )

    def build_initiative_index_document(self) -> dict[str, object]:
        return self._json_document(
            self._builder_service().build_documents(
                self._snapshot_loader.load_initiative_snapshots()
            )["initiative_index"]
        )

    def build_coordination_index_document(self) -> dict[str, object]:
        return self._json_document(
            self._builder_service().build_documents(
                self._snapshot_loader.load_initiative_snapshots()
            )["coordination_index"]
        )

    def build_task_index_document(self) -> dict[str, object]:
        return self._builder_service().build_task_index_document(
            self._snapshot_loader.load_initiative_snapshots()
        )

    def build_review_index_document(self) -> dict[str, object]:
        return self._json_document(
            self._builder_service().build_documents(
                self._snapshot_loader.load_initiative_snapshots()
            )["review_index"]
        )

    def load_task_entries(self) -> tuple[PlanTaskIndexEntry, ...]:
        document = self._load_plan_json(self._task_index_path)
        return tuple(
            PlanTaskIndexEntry.from_document(entry) for entry in self._entries(document)
        )

    def load_readiness_entries(self) -> tuple[PlanReadinessIndexEntry, ...]:
        document = self._load_plan_json(self._readiness_index_path)
        return tuple(
            PlanReadinessIndexEntry.from_document(entry)
            for entry in self._entries(document)
        )

    def load_discrepancy_entries(self) -> tuple[PlanDiscrepancyIndexEntry, ...]:
        document = self._load_plan_json(self._discrepancy_index_path)
        return tuple(
            PlanDiscrepancyIndexEntry.from_document(entry)
            for entry in self._entries(document)
        )

    def load_evidence_entries(self) -> tuple[PlanEvidenceIndexEntry, ...]:
        document = self._load_plan_json(self._evidence_index_path)
        return tuple(
            PlanEvidenceIndexEntry.from_document(entry)
            for entry in self._entries(document)
        )

    def load_closeout_entries(self) -> tuple[PlanCloseoutIndexEntry, ...]:
        document = self._load_plan_json(self._closeout_index_path)
        return tuple(
            PlanCloseoutIndexEntry.from_document(entry)
            for entry in self._entries(document)
        )

    def load_review_entries(self) -> tuple[PlanReviewIndexEntry, ...]:
        document = self._load_plan_json(self._review_index_path)
        return tuple(
            PlanReviewIndexEntry.from_document(entry)
            for entry in self._entries(document)
        )

    def load_promotion_entries(self) -> tuple[PlanPromotionIndexEntry, ...]:
        document = self._load_plan_json(self._promotion_index_path)
        return tuple(
            PlanPromotionIndexEntry.from_document(entry)
            for entry in self._entries(document)
        )

    def load_guidance_entries(self) -> tuple[PlanGuidanceIndexEntry, ...]:
        document = self._load_plan_json(self._guidance_index_path)
        return tuple(
            PlanGuidanceIndexEntry.from_document(entry)
            for entry in self._entries(document)
        )

    def search_initiatives(
        self,
        filters: RenderedSearchFilters,
    ) -> tuple[InitiativeIndexEntry, ...]:
        return search_rendered_entries(
            self.load_initiative_index().entries,
            filters,
            query_fields=initiative_rendered_query_terms,
            sort_key=lambda entry: (
                PHASE_ORDER.get(entry.current_phase, 99),
                entry.trace_id,
            ),
            trace_id=lambda entry: entry.trace_id,
            initiative_status=lambda entry: entry.initiative_status,
            current_phase=lambda entry: entry.current_phase,
            primary_owner=lambda entry: entry.primary_owner,
            active_owners=lambda entry: entry.active_owners,
            blocked_task_count=lambda entry: entry.blocked_task_count,
        )

    def search_coordination(
        self,
        filters: RenderedSearchFilters,
    ) -> tuple[InitiativeIndexEntry, ...]:
        coordination_index = self.load_coordination_index()
        entry_rank = {
            entry.trace_id: idx for idx, entry in enumerate(coordination_index.entries)
        }
        return search_rendered_entries(
            coordination_index.entries,
            filters,
            query_fields=initiative_rendered_query_terms,
            sort_key=lambda entry: (
                entry_rank.get(entry.trace_id, 9999),
                entry.trace_id,
            ),
            trace_id=lambda entry: entry.trace_id,
            initiative_status=lambda entry: entry.initiative_status,
            current_phase=lambda entry: entry.current_phase,
            primary_owner=lambda entry: entry.primary_owner,
            active_owners=lambda entry: entry.active_owners,
            blocked_task_count=lambda entry: entry.blocked_task_count,
        )

    def search_tasks(
        self, params: PlanTaskSearchParams
    ) -> tuple[PlanTaskIndexEntry, ...]:
        return search_task_entries(self.load_task_entries(), params)

    def search_readiness(
        self,
        params: PlanReadinessSearchParams,
    ) -> tuple[PlanReadinessIndexEntry, ...]:
        return search_readiness_entries(self.load_readiness_entries(), params)

    def search_discrepancies(
        self,
        params: PlanDiscrepancySearchParams,
    ) -> tuple[PlanDiscrepancyIndexEntry, ...]:
        return search_discrepancy_entries(self.load_discrepancy_entries(), params)

    def search_evidence(
        self,
        params: PlanEvidenceSearchParams,
    ) -> tuple[PlanEvidenceIndexEntry, ...]:
        return search_evidence_entries(self.load_evidence_entries(), params)

    def search_closeouts(
        self,
        params: PlanCloseoutSearchParams,
    ) -> tuple[PlanCloseoutIndexEntry, ...]:
        return search_closeout_entries(self.load_closeout_entries(), params)

    def search_reviews(
        self,
        params: PlanReviewSearchParams,
    ) -> tuple[PlanReviewIndexEntry, ...]:
        return search_review_entries(self.load_review_entries(), params)

    def _load_plan_json(self, relative_path: str) -> dict[str, object]:
        document = self._pack_loader.load_validated_document(relative_path)
        assert isinstance(document, dict)
        return document

    def _builder_service(self) -> PlanWorkspaceDocumentBuilder:
        if self._builder is None:
            vocabulary = self._vocabulary_service()
            self._renderer = PlanWorkspaceRenderer(
                repo_root=self._loader.repo_root,
                workspace_paths=self._workspace_paths,
                rendered_views=RenderedViewBuilder(self._pack_loader),
                vocabulary=vocabulary,
                overview_path=self._overview_path,
            )
            self._builder = PlanWorkspaceDocumentBuilder(
                loader=self._loader,
                pack_loader=self._pack_loader,
                workspace_paths=self._workspace_paths,
                initiative_index_path=self._initiative_index_path,
                task_index_path=self._task_index_path,
                readiness_index_path=self._readiness_index_path,
                discrepancy_index_path=self._discrepancy_index_path,
                evidence_index_path=self._evidence_index_path,
                closeout_index_path=self._closeout_index_path,
                review_index_path=self._review_index_path,
                promotion_index_path=self._promotion_index_path,
                guidance_index_path=self._guidance_index_path,
                coordination_index_path=self._coordination_index_path,
                artifact_index_path=self._artifact_index_path,
                overview_path=self._overview_path,
                evidence_bundles=EvidenceBundleHelper(self._pack_loader),
                vocabulary=vocabulary,
                renderer=self._renderer,
            )
        return self._builder

    def _refresh_pack_runtime_state(self) -> None:
        self._pack_loader = self._loader.derive(active_pack_settings_path=PLAN_PACK_SETTINGS_PATH)
        self._renderer = None
        self._builder = None
        self._markdown_reconciliation = None

    def _markdown_reconciliation_service(self) -> MarkdownReconciliationHelper:
        if self._markdown_reconciliation is None:
            self._markdown_reconciliation = MarkdownReconciliationHelper(
                self._pack_loader
            )
        return self._markdown_reconciliation

    def _vocabulary_service(self) -> TerminologyHelper:
        if self._vocabulary is None:
            self._vocabulary = TerminologyHelper.from_loader(
                self._loader,
                pack_settings_path=PLAN_PACK_SETTINGS_PATH,
            )
        return self._vocabulary

    @staticmethod
    def _json_document(value: object) -> dict[str, object]:
        return json_document(value)

    @staticmethod
    def _entries(document: dict[str, object]) -> list[dict[str, object]]:
        entries = document.get("entries", ())
        if not isinstance(entries, list):
            return []
        return [entry for entry in entries if isinstance(entry, dict)]


__all__ = [
    "INITIATIVE_PLAN_SURFACE_ID",
    "INITIATIVE_PROGRESS_SURFACE_ID",
    "INITIATIVE_SUMMARY_SURFACE_ID",
    "PLAN_ARTIFACT_INDEX_PATH",
    "PLAN_CLOSEOUT_INDEX_PATH",
    "PLAN_COORDINATION_INDEX_PATH",
    "PLAN_DISCREPANCY_INDEX_PATH",
    "PLAN_EVIDENCE_INDEX_PATH",
    "PLAN_GUIDANCE_INDEX_PATH",
    "PLAN_INITIATIVE_INDEX_PATH",
    "PLAN_OVERVIEW_PATH",
    "PLAN_OVERVIEW_SURFACE_ID",
    "PLAN_PACK_SETTINGS_PATH",
    "PLAN_PROMOTION_INDEX_PATH",
    "PLAN_READINESS_INDEX_PATH",
    "PLAN_REVIEW_INDEX_PATH",
    "PLAN_TASK_INDEX_PATH",
    "PlanCloseoutIndexEntry",
    "PlanCloseoutSearchParams",
    "PlanDiscrepancyIndexEntry",
    "PlanDiscrepancySearchParams",
    "PlanEvidenceIndexEntry",
    "PlanEvidenceSearchParams",
    "PlanGuidanceIndexEntry",
    "PlanPromotionIndexEntry",
    "PlanReadinessIndexEntry",
    "PlanReadinessSearchParams",
    "PlanReviewIndexEntry",
    "PlanReviewSearchParams",
    "PlanTaskIndexEntry",
    "PlanTaskSearchParams",
    "PlanWorkspaceService",
    "PlanWorkspaceSyncResult",
]
