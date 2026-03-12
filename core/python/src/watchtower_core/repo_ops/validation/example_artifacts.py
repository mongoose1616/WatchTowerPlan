"""Helpers for validating the governed control-plane example corpus."""

from __future__ import annotations

import json
from pathlib import Path

VALID_CONTROL_PLANE_EXAMPLES_ROOT = "core/control_plane/examples/valid"
INVALID_CONTROL_PLANE_EXAMPLES_ROOT = "core/control_plane/examples/invalid"

_DOCUMENTATION_EXAMPLE_SCHEMA_IDS = {
    "decision_record_front_matter": (
        "urn:watchtower:schema:interfaces:documentation:decision-record-front-matter:v1"
    ),
    "feature_design_front_matter": (
        "urn:watchtower:schema:interfaces:documentation:feature-design-front-matter:v1"
    ),
    "foundation_front_matter": (
        "urn:watchtower:schema:interfaces:documentation:foundation-front-matter:v1"
    ),
    "implementation_plan_front_matter": (
        "urn:watchtower:schema:interfaces:documentation:implementation-plan-front-matter:v1"
    ),
    "prd_front_matter": "urn:watchtower:schema:interfaces:documentation:prd-front-matter:v1",
    "reference_front_matter": (
        "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1"
    ),
    "standard_front_matter": (
        "urn:watchtower:schema:interfaces:documentation:standard-front-matter:v1"
    ),
    "task_front_matter": "urn:watchtower:schema:interfaces:documentation:task-front-matter:v1",
    "workflow_front_matter": (
        "urn:watchtower:schema:interfaces:documentation:workflow-front-matter:v1"
    ),
}


def iter_control_plane_example_paths(
    repo_root: Path,
    *,
    validity: str,
) -> tuple[str, ...]:
    """Return repo-relative paths for one validity partition of the example corpus."""

    if validity == "valid":
        example_root = repo_root / VALID_CONTROL_PLANE_EXAMPLES_ROOT
    elif validity == "invalid":
        example_root = repo_root / INVALID_CONTROL_PLANE_EXAMPLES_ROOT
    else:
        raise ValueError(f"Unsupported example validity: {validity}")

    return tuple(
        path.relative_to(repo_root).as_posix()
        for path in sorted(example_root.rglob("*.json"))
    )


def schema_id_for_control_plane_example(
    repo_root: Path,
    relative_path: str,
) -> str:
    """Resolve the schema ID for one governed control-plane example artifact."""

    payload = json.loads((repo_root / relative_path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{relative_path} must be a top-level JSON object example.")

    schema_id = payload.get("$schema")
    if isinstance(schema_id, str) and schema_id:
        return schema_id

    example_name = Path(relative_path).name.removesuffix(".example.json")
    for prefix, candidate in _DOCUMENTATION_EXAMPLE_SCHEMA_IDS.items():
        if example_name.startswith(prefix):
            return candidate

    raise ValueError(f"Could not resolve a schema ID for example artifact: {relative_path}")
