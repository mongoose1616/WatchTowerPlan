"""Governed surface loaders for the control-plane loader."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast

from watchtower_core.control_plane.loader_constants import (
    _MERGED_VALIDATOR_REGISTRY_CACHE_PREFIX,
    _MERGED_WORKFLOW_METADATA_REGISTRY_CACHE_PREFIX,
    _PACK_CONTEXT_CACHE_PREFIX,
    ACCEPTANCE_CONTRACTS_DIRECTORY,
    ACTOR_REGISTRY_PATH,
    AUTHORITY_MAP_PATH,
    BENCHMARK_RECORDS_DIRECTORY,
    BENCHMARK_SUITE_REGISTRY_PATH,
    COMMAND_INDEX_PATH,
    CORE_PACK_SETTINGS_PATH,
    FOUNDATION_INDEX_PATH,
    GOVERNANCE_SURFACE_MAP_PATH,
    PACK_REGISTRY_PATH,
    PACK_SETTINGS_PATH,
    PATH_PATTERN_REGISTRY_PATH,
    REFERENCE_INDEX_PATH,
    RENDERED_SURFACE_REGISTRY_PATH,
    REPOSITORY_PATH_INDEX_PATH,
    ROUTE_INDEX_PATH,
    STANDARD_INDEX_PATH,
    STATUS_REGISTRY_PATH,
    TRACEABILITY_INDEX_PATH,
    VALIDATION_EVIDENCE_DIRECTORY,
    VALIDATION_SUITE_REGISTRY_PATH,
    VALIDATOR_REGISTRY_PATH,
    WORKFLOW_INDEX_PATH,
    WORKFLOW_METADATA_REGISTRY_PATH,
    TArtifact,
)
from watchtower_core.control_plane.models import (
    AcceptanceContract,
    ActorRegistry,
    ArtifactFamilyRegistry,
    ArtifactIndex,
    AuthorityMap,
    BenchmarkRecordArtifact,
    BenchmarkSuiteRegistry,
    CommandIndex,
    CoordinationIndex,
    DocumentationFamilyRegistry,
    FoundationIndex,
    GovernanceSurfaceMap,
    HumanSurfacePolicyRegistry,
    InitiativeIndex,
    LifecycleStageRegistry,
    PackRegistry,
    PackRuntimeManifest,
    PackSettings,
    PathPatternRegistry,
    ProjectSurfacePolicyRegistry,
    PromotionPolicyRegistry,
    ReferenceIndex,
    RenderedSurfaceRegistry,
    RepositoryPathIndex,
    RetentionPolicyRegistry,
    ReviewStatusRegistry,
    RouteIndex,
    SchemaCatalog,
    SourceTypeRegistry,
    StandardIndex,
    StatusRegistry,
    TaskIndex,
    TemplateCatalog,
    TraceabilityIndex,
    ValidationEvidenceArtifact,
    ValidationSuiteRegistry,
    ValidatorRegistry,
    WorkflowIndex,
    WorkflowMetadataRegistry,
)
from watchtower_core.control_plane.pack_context import PackContext


def _load_optional_surface(
    loader: Any,
    *,
    surface_name: str,
    relative_path: str,
    default_path: str,
    builder: Callable[[dict[str, Any]], TArtifact],
) -> TArtifact:
    effective_path = loader._current_surface_path(
        surface_name,
        relative_path,
        default_path=default_path,
    )
    return cast(TArtifact, loader._load_typed_document(effective_path, builder))


def _load_required_surface(
    loader: Any,
    *,
    surface_name: str,
    relative_path: str | None,
    builder: Callable[[dict[str, Any]], TArtifact],
) -> TArtifact:
    effective_path = loader._required_surface_path(surface_name, relative_path)
    return cast(TArtifact, loader._load_typed_document(effective_path, builder))


def load_schema_catalog(loader: Any) -> SchemaCatalog:
    """Return the current typed schema catalog."""

    return cast(SchemaCatalog, loader.schema_store.catalog)


def load_validator_registry(loader: Any) -> ValidatorRegistry:
    """Load the current validator registry."""

    current_path = loader._current_validator_registry_path()
    if current_path == VALIDATOR_REGISTRY_PATH:
        return cast(
            ValidatorRegistry,
            loader._load_typed_document(
                current_path,
                ValidatorRegistry.from_document,
            ),
        )

    cache_key = "::".join(
        (
            _MERGED_VALIDATOR_REGISTRY_CACHE_PREFIX,
            VALIDATOR_REGISTRY_PATH,
            current_path,
        )
    )
    cached = loader._typed_document_cache.get(cache_key)
    if cached is not None:
        return cast(ValidatorRegistry, cached)

    core_registry = cast(
        ValidatorRegistry,
        loader._load_typed_document(
            VALIDATOR_REGISTRY_PATH,
            ValidatorRegistry.from_document,
        ),
    )
    pack_registry = cast(
        ValidatorRegistry,
        loader._load_typed_document(
            current_path,
            ValidatorRegistry.from_document,
        ),
    )
    merged_registry = ValidatorRegistry.merge(core_registry, pack_registry)
    loader._typed_document_cache[cache_key] = merged_registry
    return merged_registry


def load_validation_suite_registry(loader: Any) -> ValidationSuiteRegistry:
    """Load the current validation-suite registry."""

    return cast(
        ValidationSuiteRegistry,
        loader._load_typed_document(
            loader._current_validation_suite_registry_path(),
            ValidationSuiteRegistry.from_document,
        ),
    )


def load_benchmark_suite_registry(loader: Any) -> BenchmarkSuiteRegistry:
    """Load the current benchmark-suite registry."""

    return cast(
        BenchmarkSuiteRegistry,
        loader._load_typed_document(
            loader._current_benchmark_suite_registry_path(),
            BenchmarkSuiteRegistry.from_document,
        ),
    )


def load_pack_registry(
    loader: Any,
    relative_path: str = PACK_REGISTRY_PATH,
) -> PackRegistry:
    """Load the hosted-pack registry."""

    return cast(
        PackRegistry,
        loader._load_typed_document(relative_path, PackRegistry.from_document),
    )


def load_pack_settings(
    loader: Any,
    relative_path: str = PACK_SETTINGS_PATH,
) -> PackSettings:
    """Load one typed pack-settings surface."""

    effective_path = loader._current_pack_settings_path(relative_path)
    return cast(
        PackSettings,
        loader._load_typed_document(effective_path, PackSettings.from_document),
    )


def load_pack_runtime_manifest(
    loader: Any,
    relative_path: str | None = None,
    *,
    pack_settings_path: str = PACK_SETTINGS_PATH,
) -> PackRuntimeManifest:
    """Load one typed pack-runtime manifest."""

    effective_path = (
        loader.pack_runtime_manifest_path(loader.activate_pack_settings(pack_settings_path))
        if relative_path is None
        else loader._current_pack_settings_path(relative_path)
    )
    return cast(
        PackRuntimeManifest,
        loader._load_typed_document(effective_path, PackRuntimeManifest.from_document),
    )


def load_governance_surface_map(
    loader: Any,
    relative_path: str = GOVERNANCE_SURFACE_MAP_PATH,
) -> GovernanceSurfaceMap:
    """Load one typed governance-surface map."""

    return _load_optional_surface(
        loader,
        surface_name="governance_surface_map",
        relative_path=relative_path,
        default_path=GOVERNANCE_SURFACE_MAP_PATH,
        builder=GovernanceSurfaceMap.from_document,
    )


def load_path_pattern_registry(
    loader: Any,
    relative_path: str = PATH_PATTERN_REGISTRY_PATH,
) -> PathPatternRegistry:
    """Load one typed path-pattern registry."""

    return _load_optional_surface(
        loader,
        surface_name="path_pattern_registry",
        relative_path=relative_path,
        default_path=PATH_PATTERN_REGISTRY_PATH,
        builder=PathPatternRegistry.from_document,
    )


def load_status_registry(
    loader: Any,
    relative_path: str = STATUS_REGISTRY_PATH,
) -> StatusRegistry:
    """Load one typed status registry."""

    return _load_optional_surface(
        loader,
        surface_name="status_registry",
        relative_path=relative_path,
        default_path=STATUS_REGISTRY_PATH,
        builder=StatusRegistry.from_document,
    )


def load_actor_registry(
    loader: Any,
    relative_path: str = ACTOR_REGISTRY_PATH,
) -> ActorRegistry:
    """Load one typed actor registry."""

    return _load_optional_surface(
        loader,
        surface_name="actor_registry",
        relative_path=relative_path,
        default_path=ACTOR_REGISTRY_PATH,
        builder=ActorRegistry.from_document,
    )


def load_authority_map(loader: Any) -> AuthorityMap:
    """Load the current authority-map registry."""

    return _load_optional_surface(
        loader,
        surface_name="authority_map",
        relative_path=AUTHORITY_MAP_PATH,
        default_path=AUTHORITY_MAP_PATH,
        builder=AuthorityMap.from_document,
    )


def load_rendered_surface_registry(loader: Any) -> RenderedSurfaceRegistry:
    """Load the current rendered-surface registry."""

    return _load_optional_surface(
        loader,
        surface_name="rendered_surface_registry",
        relative_path=RENDERED_SURFACE_REGISTRY_PATH,
        default_path=RENDERED_SURFACE_REGISTRY_PATH,
        builder=RenderedSurfaceRegistry.from_document,
    )


def load_workflow_metadata_registry(loader: Any) -> WorkflowMetadataRegistry:
    """Load the current workflow metadata registry."""
    current_path = loader._current_surface_path(
        "workflow_metadata_registry",
        WORKFLOW_METADATA_REGISTRY_PATH,
        default_path=WORKFLOW_METADATA_REGISTRY_PATH,
    )
    if current_path == WORKFLOW_METADATA_REGISTRY_PATH:
        return cast(
            WorkflowMetadataRegistry,
            loader._load_typed_document(
                current_path,
                WorkflowMetadataRegistry.from_document,
            ),
        )

    cache_key = "::".join(
        (
            _MERGED_WORKFLOW_METADATA_REGISTRY_CACHE_PREFIX,
            WORKFLOW_METADATA_REGISTRY_PATH,
            current_path,
        )
    )
    cached = loader._typed_document_cache.get(cache_key)
    if cached is not None:
        return cast(WorkflowMetadataRegistry, cached)

    core_registry = cast(
        WorkflowMetadataRegistry,
        loader._load_typed_document(
            WORKFLOW_METADATA_REGISTRY_PATH,
            WorkflowMetadataRegistry.from_document,
        ),
    )
    pack_registry = cast(
        WorkflowMetadataRegistry,
        loader._load_typed_document(
            current_path,
            WorkflowMetadataRegistry.from_document,
        ),
    )
    merged_registry = WorkflowMetadataRegistry.merge(core_registry, pack_registry)
    loader._typed_document_cache[cache_key] = merged_registry
    return merged_registry


def load_documentation_family_registry(
    loader: Any,
    relative_path: str | None = None,
) -> DocumentationFamilyRegistry:
    """Load the current documentation-family registry."""

    return _load_required_surface(
        loader,
        surface_name="documentation_family_registry",
        relative_path=relative_path,
        builder=DocumentationFamilyRegistry.from_document,
    )


def load_template_catalog(
    loader: Any,
    relative_path: str | None = None,
) -> TemplateCatalog:
    """Load the current template catalog."""

    return _load_required_surface(
        loader,
        surface_name="template_catalog",
        relative_path=relative_path,
        builder=TemplateCatalog.from_document,
    )


def load_artifact_family_registry(
    loader: Any,
    relative_path: str | None = None,
) -> ArtifactFamilyRegistry:
    """Load the current artifact-family registry."""

    return _load_required_surface(
        loader,
        surface_name="artifact_family_registry",
        relative_path=relative_path,
        builder=ArtifactFamilyRegistry.from_document,
    )


def load_lifecycle_stage_registry(
    loader: Any,
    relative_path: str | None = None,
) -> LifecycleStageRegistry:
    """Load the current lifecycle-stage registry."""

    return _load_required_surface(
        loader,
        surface_name="lifecycle_stage_registry",
        relative_path=relative_path,
        builder=LifecycleStageRegistry.from_document,
    )


def load_review_status_registry(
    loader: Any,
    relative_path: str | None = None,
) -> ReviewStatusRegistry:
    """Load the current review-status registry."""

    return _load_required_surface(
        loader,
        surface_name="review_status_registry",
        relative_path=relative_path,
        builder=ReviewStatusRegistry.from_document,
    )


def load_source_type_registry(
    loader: Any,
    relative_path: str | None = None,
) -> SourceTypeRegistry:
    """Load the current source-type registry."""

    return _load_required_surface(
        loader,
        surface_name="source_type_registry",
        relative_path=relative_path,
        builder=SourceTypeRegistry.from_document,
    )


def load_promotion_policy_registry(
    loader: Any,
    relative_path: str | None = None,
) -> PromotionPolicyRegistry:
    """Load the current promotion-policy registry."""

    return _load_required_surface(
        loader,
        surface_name="promotion_policy_registry",
        relative_path=relative_path,
        builder=PromotionPolicyRegistry.from_document,
    )


def load_project_surface_policy_registry(
    loader: Any,
    relative_path: str | None = None,
) -> ProjectSurfacePolicyRegistry:
    """Load the current project-surface policy registry."""

    return _load_required_surface(
        loader,
        surface_name="project_surface_policy_registry",
        relative_path=relative_path,
        builder=ProjectSurfacePolicyRegistry.from_document,
    )


def load_human_surface_policy_registry(
    loader: Any,
    relative_path: str | None = None,
) -> HumanSurfacePolicyRegistry:
    """Load the current human-surface policy registry."""

    return _load_required_surface(
        loader,
        surface_name="human_surface_policy_registry",
        relative_path=relative_path,
        builder=HumanSurfacePolicyRegistry.from_document,
    )


def load_retention_policy_registry(
    loader: Any,
    relative_path: str | None = None,
) -> RetentionPolicyRegistry:
    """Load the current retention-policy registry."""

    return _load_required_surface(
        loader,
        surface_name="retention_policy_registry",
        relative_path=relative_path,
        builder=RetentionPolicyRegistry.from_document,
    )


def load_artifact_index(
    loader: Any,
    relative_path: str | None = None,
) -> ArtifactIndex:
    """Load the current pack artifact index."""

    return _load_required_surface(
        loader,
        surface_name="artifact_index",
        relative_path=relative_path,
        builder=ArtifactIndex.from_document,
    )


def load_repository_path_index(loader: Any) -> RepositoryPathIndex:
    """Load the current repository path index."""

    return cast(
        RepositoryPathIndex,
        loader._load_typed_document(
            REPOSITORY_PATH_INDEX_PATH,
            RepositoryPathIndex.from_document,
        ),
    )


def load_command_index(loader: Any) -> CommandIndex:
    """Load the current command index."""

    return cast(
        CommandIndex,
        loader._load_typed_document(COMMAND_INDEX_PATH, CommandIndex.from_document),
    )


def load_route_index(loader: Any) -> RouteIndex:
    """Load the current route index."""

    return cast(
        RouteIndex,
        loader._load_typed_document(ROUTE_INDEX_PATH, RouteIndex.from_document),
    )


def load_reference_index(loader: Any) -> ReferenceIndex:
    """Load the current reference index."""

    return cast(
        ReferenceIndex,
        loader._load_typed_document(REFERENCE_INDEX_PATH, ReferenceIndex.from_document),
    )


def load_foundation_index(loader: Any) -> FoundationIndex:
    """Load the current foundation index."""

    return cast(
        FoundationIndex,
        loader._load_typed_document(FOUNDATION_INDEX_PATH, FoundationIndex.from_document),
    )


def load_initiative_index(loader: Any) -> InitiativeIndex:
    """Load the current initiative index."""

    return _load_required_surface(
        loader,
        surface_name="initiative_index",
        relative_path=None,
        builder=InitiativeIndex.from_document,
    )


def load_coordination_index(loader: Any) -> CoordinationIndex:
    """Load the current coordination index."""

    return _load_required_surface(
        loader,
        surface_name="coordination_index",
        relative_path=None,
        builder=CoordinationIndex.from_document,
    )


def load_standard_index(loader: Any) -> StandardIndex:
    """Load the current standard index."""

    return cast(
        StandardIndex,
        loader._load_typed_document(STANDARD_INDEX_PATH, StandardIndex.from_document),
    )


def load_workflow_index(loader: Any) -> WorkflowIndex:
    """Load the current workflow index."""

    return cast(
        WorkflowIndex,
        loader._load_typed_document(WORKFLOW_INDEX_PATH, WorkflowIndex.from_document),
    )


def load_task_index(loader: Any) -> TaskIndex:
    """Load the current task index."""

    return _load_required_surface(
        loader,
        surface_name="task_index",
        relative_path=None,
        builder=TaskIndex.from_document,
    )


def load_traceability_index(loader: Any) -> TraceabilityIndex:
    """Load the current traceability index."""

    return cast(
        TraceabilityIndex,
        loader._load_typed_document(
            TRACEABILITY_INDEX_PATH,
            TraceabilityIndex.from_document,
        ),
    )


def load_acceptance_contracts(loader: Any) -> tuple[AcceptanceContract, ...]:
    """Load all governed acceptance-contract artifacts."""

    return cast(
        tuple[AcceptanceContract, ...],
        loader._load_typed_directory(
            ACCEPTANCE_CONTRACTS_DIRECTORY,
            lambda relative_path, document: AcceptanceContract.from_document(
                document,
                doc_path=relative_path,
            ),
        ),
    )


def load_validation_evidence_artifacts(
    loader: Any,
) -> tuple[ValidationEvidenceArtifact, ...]:
    """Load all governed validation-evidence artifacts."""

    return cast(
        tuple[ValidationEvidenceArtifact, ...],
        loader._load_typed_directory(
            VALIDATION_EVIDENCE_DIRECTORY,
            lambda relative_path, document: ValidationEvidenceArtifact.from_document(
                document,
                doc_path=relative_path,
            ),
        ),
    )


def load_benchmark_record_artifacts(
    loader: Any,
) -> tuple[BenchmarkRecordArtifact, ...]:
    """Load all governed benchmark record artifacts."""

    return cast(
        tuple[BenchmarkRecordArtifact, ...],
        loader._load_typed_directory(
            BENCHMARK_RECORDS_DIRECTORY,
            lambda relative_path, document: BenchmarkRecordArtifact.from_document(
                document,
                doc_path=relative_path,
            ),
        ),
    )


def load_pack_context(
    loader: Any,
    pack_settings_path: str = PACK_SETTINGS_PATH,
) -> PackContext:
    """Load one PackContext from pack settings and its declared governed surfaces."""

    if pack_settings_path == PACK_SETTINGS_PATH:
        return cast(PackContext, loader.load_active_pack_context(pack_settings_path))
    effective_pack_settings_path = loader._current_pack_settings_path(pack_settings_path)
    if loader.active_pack_settings_path == effective_pack_settings_path:
        return cast(PackContext, loader.load_active_pack_context(pack_settings_path))
    return PackContext.from_loader(
        loader,
        pack_settings_path=effective_pack_settings_path,
    )


def load_active_pack_context(
    loader: Any,
    pack_settings_path: str = PACK_SETTINGS_PATH,
) -> PackContext:
    """Activate and cache the effective PackContext for one pack-aware operation."""

    effective_pack_settings_path = loader.activate_pack_settings(pack_settings_path)
    cache_key = _pack_context_cache_key(loader, effective_pack_settings_path)
    cached = loader._typed_document_cache.get(cache_key)
    if cached is not None:
        return cast(PackContext, cached)
    context = PackContext.from_loader(
        loader,
        pack_settings_path=effective_pack_settings_path,
    )
    loader._typed_document_cache[cache_key] = context
    return context


def _pack_context_cache_key(loader: Any, pack_settings_path: str) -> str:
    """Build one cache key that invalidates with the pack settings and declared surfaces."""

    pack_settings = loader.load_pack_settings(pack_settings_path)
    surface_paths = tuple(declaration.path for declaration in pack_settings.surfaces)
    return "::".join((_PACK_CONTEXT_CACHE_PREFIX, pack_settings_path, *surface_paths))


def _declared_surface_loaders(loader: Any) -> dict[str, Callable[[str], object]]:
    return {
        "schema_catalog": lambda relative_path: loader._load_typed_document(
            relative_path,
            lambda document: SchemaCatalog.from_document(document, loader.workspace_config),
        ),
        "validator_registry": lambda relative_path: loader.load_validator_registry(),
        "validation_suite_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            ValidationSuiteRegistry.from_document,
        ),
        "benchmark_suite_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            BenchmarkSuiteRegistry.from_document,
        ),
        "authority_map": lambda relative_path: loader._load_typed_document(
            relative_path,
            AuthorityMap.from_document,
        ),
        "rendered_surface_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            RenderedSurfaceRegistry.from_document,
        ),
        "workflow_metadata_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            WorkflowMetadataRegistry.from_document,
        ),
        "documentation_family_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            DocumentationFamilyRegistry.from_document,
        ),
        "template_catalog": lambda relative_path: loader._load_typed_document(
            relative_path,
            TemplateCatalog.from_document,
        ),
        "artifact_family_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            ArtifactFamilyRegistry.from_document,
        ),
        "lifecycle_stage_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            LifecycleStageRegistry.from_document,
        ),
        "review_status_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            ReviewStatusRegistry.from_document,
        ),
        "source_type_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            SourceTypeRegistry.from_document,
        ),
        "promotion_policy_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            PromotionPolicyRegistry.from_document,
        ),
        "project_surface_policy_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            ProjectSurfacePolicyRegistry.from_document,
        ),
        "human_surface_policy_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            HumanSurfacePolicyRegistry.from_document,
        ),
        "retention_policy_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            RetentionPolicyRegistry.from_document,
        ),
        "artifact_index": lambda relative_path: loader._load_typed_document(
            relative_path,
            ArtifactIndex.from_document,
        ),
        "pack_settings": lambda relative_path: loader._load_typed_document(
            relative_path,
            PackSettings.from_document,
        ),
        "governance_surface_map": lambda relative_path: loader._load_typed_document(
            relative_path,
            GovernanceSurfaceMap.from_document,
        ),
        "path_pattern_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            PathPatternRegistry.from_document,
        ),
        "status_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            StatusRegistry.from_document,
        ),
        "actor_registry": lambda relative_path: loader._load_typed_document(
            relative_path,
            ActorRegistry.from_document,
        ),
        "repository_path_index": lambda relative_path: loader._load_typed_document(
            relative_path,
            RepositoryPathIndex.from_document,
        ),
        "command_index": lambda relative_path: loader._load_typed_document(
            relative_path,
            CommandIndex.from_document,
        ),
        "route_index": lambda relative_path: loader._load_typed_document(
            relative_path,
            RouteIndex.from_document,
        ),
        "reference_index": lambda relative_path: loader._load_typed_document(
            relative_path,
            ReferenceIndex.from_document,
        ),
        "foundation_index": lambda relative_path: loader._load_typed_document(
            relative_path,
            FoundationIndex.from_document,
        ),
        "initiative_index": lambda relative_path: loader._load_typed_document(
            relative_path,
            InitiativeIndex.from_document,
        ),
        "coordination_index": lambda relative_path: loader._load_typed_document(
            relative_path,
            CoordinationIndex.from_document,
        ),
        "standard_index": lambda relative_path: loader._load_typed_document(
            relative_path,
            StandardIndex.from_document,
        ),
        "workflow_index": lambda relative_path: loader._load_typed_document(
            relative_path,
            WorkflowIndex.from_document,
        ),
        "task_index": lambda relative_path: loader._load_typed_document(
            relative_path,
            TaskIndex.from_document,
        ),
        "traceability_index": lambda relative_path: loader._load_typed_document(
            relative_path,
            TraceabilityIndex.from_document,
        ),
    }


def load_declared_surface(
    loader: Any,
    *,
    surface_name: str,
    relative_path: str,
) -> object:
    """Load one pack-declared surface as a typed artifact when the surface is known."""

    surface_loader = _declared_surface_loaders(loader).get(surface_name)
    if surface_loader is not None:
        return surface_loader(relative_path)
    return loader.load_known_surface(relative_path)


def load_known_surface(loader: Any, relative_path: str) -> object:
    """Load one known governed surface as a typed artifact when available."""

    if relative_path == PACK_SETTINGS_PATH:
        return loader.load_pack_settings()
    if relative_path == CORE_PACK_SETTINGS_PATH:
        return loader.load_pack_settings(CORE_PACK_SETTINGS_PATH)
    if relative_path == loader.default_pack_settings_path():
        return loader.load_pack_settings(relative_path)
    if (
        loader.active_pack_settings_path is not None
        and relative_path == loader.active_pack_settings_path
    ):
        return loader.load_pack_settings(relative_path)
    active_surface_name = loader._surface_name_for_active_path(relative_path)
    if active_surface_name is not None:
        return loader.load_declared_surface(
            surface_name=active_surface_name,
            relative_path=relative_path,
        )

    known_surfaces: dict[str, Callable[[], object]] = {
        VALIDATOR_REGISTRY_PATH: loader.load_validator_registry,
        VALIDATION_SUITE_REGISTRY_PATH: loader.load_validation_suite_registry,
        BENCHMARK_SUITE_REGISTRY_PATH: loader.load_benchmark_suite_registry,
        PACK_REGISTRY_PATH: loader.load_pack_registry,
        AUTHORITY_MAP_PATH: loader.load_authority_map,
        RENDERED_SURFACE_REGISTRY_PATH: loader.load_rendered_surface_registry,
        WORKFLOW_METADATA_REGISTRY_PATH: loader.load_workflow_metadata_registry,
        GOVERNANCE_SURFACE_MAP_PATH: loader.load_governance_surface_map,
        PATH_PATTERN_REGISTRY_PATH: loader.load_path_pattern_registry,
        STATUS_REGISTRY_PATH: loader.load_status_registry,
        ACTOR_REGISTRY_PATH: loader.load_actor_registry,
        REPOSITORY_PATH_INDEX_PATH: loader.load_repository_path_index,
        COMMAND_INDEX_PATH: loader.load_command_index,
        ROUTE_INDEX_PATH: loader.load_route_index,
        REFERENCE_INDEX_PATH: loader.load_reference_index,
        FOUNDATION_INDEX_PATH: loader.load_foundation_index,
        STANDARD_INDEX_PATH: loader.load_standard_index,
        WORKFLOW_INDEX_PATH: loader.load_workflow_index,
        TRACEABILITY_INDEX_PATH: loader.load_traceability_index,
        "core/control_plane/registries/schema_catalog.json": loader.load_schema_catalog,
    }
    surface_loader = known_surfaces.get(relative_path)
    if surface_loader is not None:
        return surface_loader()
    if relative_path == loader.pack_runtime_manifest_path():
        return loader.load_pack_runtime_manifest(relative_path=relative_path)
    return loader.load_validated_document(relative_path)
