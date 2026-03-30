"""Shared constants for governed control-plane loading."""

from __future__ import annotations

from typing import TypeVar

VALIDATOR_REGISTRY_PATH = "core/control_plane/registries/validator_registry.json"
VALIDATION_SUITE_REGISTRY_PATH = "core/control_plane/registries/validation_suite_registry.json"
BENCHMARK_SUITE_REGISTRY_PATH = "core/control_plane/registries/benchmark_suite_registry.json"
SCHEMA_CATALOG_ARTIFACT_PATH = "core/control_plane/registries/schema_catalog.json"
PACK_REGISTRY_PATH = "core/control_plane/registries/pack_registry.json"
AUTHORITY_MAP_PATH = "core/control_plane/registries/authority_map.json"
WORKFLOW_METADATA_REGISTRY_PATH = "core/control_plane/registries/workflow_metadata_registry.json"
PACK_SETTINGS_PATH = "__active_pack_settings__"
CORE_PACK_SETTINGS_PATH = "core/control_plane/manifests/pack_settings.json"
PACK_RUNTIME_MANIFEST_FILENAME = "pack_runtime_manifest.json"
GOVERNANCE_SURFACE_MAP_PATH = "core/control_plane/registries/governance_surface_map.json"
PATH_PATTERN_REGISTRY_PATH = "core/control_plane/registries/path_pattern_registry.json"
STATUS_REGISTRY_PATH = "core/control_plane/registries/status_registry.json"
ACTOR_REGISTRY_PATH = "core/control_plane/registries/actor_registry.json"
RENDERED_SURFACE_REGISTRY_PATH = "core/control_plane/registries/rendered_surface_registry.json"
REPOSITORY_PATH_INDEX_PATH = (
    "core/control_plane/indexes/repository_paths/repository_path_index.json"
)
COMMAND_INDEX_PATH = "core/control_plane/indexes/commands/command_index.json"
ROUTE_INDEX_PATH = "core/control_plane/indexes/routes/route_index.json"
REFERENCE_INDEX_PATH = "core/control_plane/indexes/references/reference_index.json"
FOUNDATION_INDEX_PATH = "core/control_plane/indexes/foundations/foundation_index.json"
STANDARD_INDEX_PATH = "core/control_plane/indexes/standards/standard_index.json"
WORKFLOW_INDEX_PATH = "core/control_plane/indexes/workflows/workflow_index.json"
TRACEABILITY_INDEX_PATH = "core/control_plane/indexes/traceability/traceability_index.json"
ACCEPTANCE_CONTRACTS_DIRECTORY = "core/control_plane/contracts/acceptance"
BENCHMARK_RECORDS_DIRECTORY = "core/control_plane/records/benchmarks"
VALIDATION_EVIDENCE_DIRECTORY = "core/control_plane/records/validation_evidence"

TArtifact = TypeVar("TArtifact")
_KEEP_ACTIVE_PACK_SETTINGS = object()
_PACK_CONTEXT_CACHE_PREFIX = "__pack_context__"
_MERGED_VALIDATOR_REGISTRY_CACHE_PREFIX = "__merged_validator_registry__"
_MERGED_WORKFLOW_METADATA_REGISTRY_CACHE_PREFIX = "__merged_workflow_metadata_registry__"
