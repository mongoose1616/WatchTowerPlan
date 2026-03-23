"""Reusable scaffold helpers for hosted pack starter generation."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from watchtower_core.pack_integration.workspace_registration import (
    core_python_workspace_registration,
)
from watchtower_core.utils.timestamps import utc_timestamp_now

_PACK_TEMPLATES_ROOT = Path("core/docs/templates/pack")
_SLUG_RE = re.compile(r"^[a-z][a-z0-9-]*$")
_DOMAIN_ROOT_RE = re.compile(r"^[a-z][a-z0-9_-]*$")


@dataclass(frozen=True, slots=True)
class PackScaffoldRequest:
    """Parameters for generating one hosted-pack starter."""

    pack_slug: str
    pack_root: str
    command_namespace: str | None = None
    python_distribution: str | None = None
    python_package: str | None = None
    domain_root_names: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class PackScaffoldResult:
    """Summary of one generated hosted-pack starter."""

    pack_slug: str
    pack_root: str
    command_namespace: str
    python_distribution: str
    python_package: str
    pack_settings_path: str
    pack_runtime_manifest_path: str
    created_paths: tuple[str, ...]
    pack_registry_entry: dict[str, object]
    core_python_dependency: str
    core_python_uv_source: dict[str, object]


@dataclass(frozen=True, slots=True)
class _ResolvedPackScaffold:
    pack_slug: str
    pack_title: str
    pack_root: str
    command_namespace: str
    python_distribution: str
    python_package: str
    note_slug: str
    schema_slug: str
    pack_settings_path: str
    pack_runtime_manifest_path: str
    domain_roots: dict[str, str]
    updated_at: str


def scaffold_hosted_pack(
    repo_root: Path,
    request: PackScaffoldRequest,
) -> PackScaffoldResult:
    """Create a pack-owned starter surface set under one repository root."""

    resolved = _resolve_request(request)
    _validate_repo_state(repo_root, resolved)

    created_paths: list[str] = []
    _write_scaffold_files(repo_root, resolved, created_paths)
    workspace_registration = core_python_workspace_registration(
        repo_root,
        python_root=f"{resolved.pack_root}/python",
        python_distribution=resolved.python_distribution,
    )

    return PackScaffoldResult(
        pack_slug=resolved.pack_slug,
        pack_root=resolved.pack_root,
        command_namespace=resolved.command_namespace,
        python_distribution=resolved.python_distribution,
        python_package=resolved.python_package,
        pack_settings_path=resolved.pack_settings_path,
        pack_runtime_manifest_path=resolved.pack_runtime_manifest_path,
        created_paths=tuple(created_paths),
        pack_registry_entry=_pack_registry_entry(resolved),
        core_python_dependency=workspace_registration.dependency,
        core_python_uv_source={
            "path": workspace_registration.uv_source_path,
            "editable": workspace_registration.editable,
        },
    )


def _resolve_request(request: PackScaffoldRequest) -> _ResolvedPackScaffold:
    pack_slug = request.pack_slug.strip()
    if not _SLUG_RE.fullmatch(pack_slug):
        raise ValueError(
            "pack_slug must be lowercase letters, digits, and hyphens only, and "
            "must start with a letter."
        )
    command_namespace = (request.command_namespace or pack_slug).strip()
    if not _SLUG_RE.fullmatch(command_namespace):
        raise ValueError(
            "command_namespace must be lowercase letters, digits, and hyphens only, "
            "and must start with a letter."
        )
    pack_root = _validate_relative_root(request.pack_root)
    python_distribution = (request.python_distribution or f"watchtower-{pack_slug}").strip()
    python_package = (request.python_package or f"watchtower_{pack_slug.replace('-', '_')}").strip()
    if not python_package.startswith("watchtower_"):
        raise ValueError("python_package must stay under the watchtower_<pack> namespace.")
    domain_roots: dict[str, str] = {}
    for name in request.domain_root_names:
        normalized_name = name.strip()
        if not _DOMAIN_ROOT_RE.fullmatch(normalized_name):
            raise ValueError(
                "domain_root_names must be lowercase letters, digits, underscores, or "
                "hyphens only, and must start with a letter."
            )
        domain_roots[normalized_name] = f"{pack_root}/{normalized_name}"
    return _ResolvedPackScaffold(
        pack_slug=pack_slug,
        pack_title=pack_slug.replace("-", " ").title(),
        pack_root=pack_root,
        command_namespace=command_namespace,
        python_distribution=python_distribution,
        python_package=python_package,
        note_slug=f"{pack_slug.replace('-', '_')}_note",
        schema_slug=f"{pack_slug}-note",
        pack_settings_path=f"{pack_root}/.wt/manifests/pack_settings.json",
        pack_runtime_manifest_path=f"{pack_root}/.wt/manifests/pack_runtime_manifest.json",
        domain_roots=domain_roots,
        updated_at=utc_timestamp_now(),
    )


def _validate_relative_root(pack_root: str) -> str:
    candidate = PurePosixPath(pack_root.strip())
    if not pack_root.strip():
        raise ValueError("pack_root is required.")
    if candidate.is_absolute() or any(part == ".." for part in candidate.parts):
        raise ValueError("pack_root must stay repository-relative and portable.")
    return candidate.as_posix()


def _validate_repo_state(repo_root: Path, resolved: _ResolvedPackScaffold) -> None:
    pack_root_path = repo_root / resolved.pack_root
    if pack_root_path.exists():
        raise ValueError(f"pack_root already exists: {resolved.pack_root}")
    pack_registry_path = repo_root / "core/control_plane/registries/pack_registry.json"
    pack_registry = json.loads(pack_registry_path.read_text(encoding="utf-8"))
    for entry in pack_registry.get("packs", ()):
        if (
            entry["pack_id"] == f"pack.{resolved.pack_slug}"
            or entry["pack_slug"] == resolved.pack_slug
        ):
            raise ValueError(f"Hosted pack already exists in pack_registry: {resolved.pack_slug}")
        if entry["command_namespace"] == resolved.command_namespace:
            raise ValueError(
                "Hosted pack command namespace already exists in pack_registry: "
                f"{resolved.command_namespace}"
            )
        if entry["python_distribution"] == resolved.python_distribution:
            raise ValueError(
                "Hosted pack python_distribution already exists in pack_registry: "
                f"{resolved.python_distribution}"
            )
        if entry["python_package"] == resolved.python_package:
            raise ValueError(
                "Hosted pack python_package already exists in pack_registry: "
                f"{resolved.python_package}"
            )


def _write_scaffold_files(
    repo_root: Path,
    resolved: _ResolvedPackScaffold,
    created_paths: list[str],
) -> None:
    replacements = _template_replacements(resolved)
    template_writes = (
        (
            "pack_settings_template.json",
            resolved.pack_settings_path,
            _render_with_domain_roots(
                _load_template(repo_root, "pack_settings_template.json"),
                domain_roots=resolved.domain_roots,
                field_name="workspace_roots",
            ),
        ),
        (
            "pack_runtime_manifest_template.json",
            resolved.pack_runtime_manifest_path,
            _render_with_domain_roots(
                _load_template(repo_root, "pack_runtime_manifest_template.json"),
                domain_roots=resolved.domain_roots,
                field_name="owned_roots",
            ),
        ),
        (
            "pack_schema_catalog_template.json",
            f"{resolved.pack_root}/.wt/registries/schema_catalog.json",
            _load_template(repo_root, "pack_schema_catalog_template.json"),
        ),
        (
            "pack_validation_suite_registry_template.json",
            f"{resolved.pack_root}/.wt/registries/validation_suite_registry.json",
            _load_template(repo_root, "pack_validation_suite_registry_template.json"),
        ),
        (
            "pack_workflow_metadata_registry_template.json",
            f"{resolved.pack_root}/.wt/registries/workflow_metadata_registry.json",
            _load_template(repo_root, "pack_workflow_metadata_registry_template.json"),
        ),
        (
            "pack_validator_registry_template.json",
            f"{resolved.pack_root}/.wt/registries/validator_registry.json",
            _load_template(repo_root, "pack_validator_registry_template.json"),
        ),
        (
            "pack_note_schema_template.json",
            f"{resolved.pack_root}/.wt/schemas/interfaces/packs/{resolved.note_slug}.schema.json",
            _load_template(repo_root, "pack_note_schema_template.json"),
        ),
        (
            "pack_note_artifact_template.json",
            f"{resolved.pack_root}/.wt/work_items/{resolved.note_slug}.json",
            _load_template(repo_root, "pack_note_artifact_template.json"),
        ),
        (
            "pack_namespace_command_reference_template.md",
            (
                f"{resolved.pack_root}/docs/commands/core_python/"
                f"watchtower_core_{resolved.command_namespace.replace('-', '_')}.md"
            ),
            _namespace_command_reference(resolved),
        ),
        (
            "pack_python_pyproject_template.toml",
            f"{resolved.pack_root}/python/pyproject.toml",
            _load_template(repo_root, "pack_python_pyproject_template.toml"),
        ),
        (
            "pack_package_init_template.py",
            f"{resolved.pack_root}/python/src/{resolved.python_package}/__init__.py",
            _load_template(repo_root, "pack_package_init_template.py"),
        ),
        (
            "pack_integration_module_template.py",
            f"{resolved.pack_root}/python/src/{resolved.python_package}/integration.py",
            _load_template(repo_root, "pack_integration_module_template.py"),
        ),
    )
    for _, relative_path, template_text in template_writes:
        _write_text(
            repo_root,
            relative_path,
            _apply_replacements(template_text, replacements),
            created_paths,
        )

    _write_text(
        repo_root,
        f"{resolved.pack_root}/README.md",
        _pack_root_readme(resolved),
        created_paths,
    )
    _write_text(
        repo_root,
        f"{resolved.pack_root}/docs/README.md",
        _docs_readme(resolved),
        created_paths,
    )
    _write_text(
        repo_root,
        f"{resolved.pack_root}/workflows/README.md",
        _workflows_readme(resolved),
        created_paths,
    )
    _write_text(
        repo_root,
        f"{resolved.pack_root}/workflows/ROUTING_TABLE.md",
        _workflow_routing_table(resolved),
        created_paths,
    )
    _write_text(
        repo_root,
        f"{resolved.pack_root}/tracking/README.md",
        _tracking_readme(resolved),
        created_paths,
    )
    _write_text(
        repo_root,
        f"{resolved.pack_root}/python/README.md",
        _python_readme(resolved),
        created_paths,
    )
    for root_name, relative_root in resolved.domain_roots.items():
        _write_text(
            repo_root,
            f"{relative_root}/README.md",
            _domain_root_readme(resolved, root_name, relative_root),
            created_paths,
        )


def _template_replacements(resolved: _ResolvedPackScaffold) -> tuple[tuple[str, str], ...]:
    return (
        ("<pack_slug>", resolved.pack_slug),
        ("<pack_title>", resolved.pack_title),
        ("<command_namespace>", resolved.command_namespace),
        ("<pack_root>", resolved.pack_root),
        ("<schema_slug>", resolved.schema_slug),
        ("<note_slug>", resolved.note_slug),
        ("<python_package>", resolved.python_package),
        (
            "<pack_root>/python/src/watchtower_<pack_slug>",
            f"{resolved.pack_root}/python/src/{resolved.python_package}",
        ),
        ("watchtower_<pack_slug>", resolved.python_package),
        ("watchtower-<pack_slug>", resolved.python_distribution),
        ("YYYY-MM-DDTHH:MM:SSZ", resolved.updated_at),
    )


def _load_template(repo_root: Path, filename: str) -> str:
    path = repo_root / _PACK_TEMPLATES_ROOT / filename
    return path.read_text(encoding="utf-8")


def _apply_replacements(
    template_text: str,
    replacements: tuple[tuple[str, str], ...],
) -> str:
    rendered = template_text
    for old, new in replacements:
        rendered = rendered.replace(old, new)
    return rendered


def _render_with_domain_roots(
    template_text: str,
    *,
    domain_roots: dict[str, str],
    field_name: str,
) -> str:
    document = json.loads(template_text)
    document[field_name]["domain_roots"] = domain_roots
    return f"{json.dumps(document, indent=2)}\n"


def _write_text(
    repo_root: Path,
    relative_path: str,
    text: str,
    created_paths: list[str],
) -> None:
    path = repo_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith("\n") else f"{text}\n", encoding="utf-8")
    created_paths.append(relative_path)


def _pack_registry_entry(resolved: _ResolvedPackScaffold) -> dict[str, object]:
    return {
        "pack_id": f"pack.{resolved.pack_slug}",
        "pack_slug": resolved.pack_slug,
        "command_namespace": resolved.command_namespace,
        "pack_settings_path": resolved.pack_settings_path,
        "pack_runtime_manifest_path": resolved.pack_runtime_manifest_path,
        "python_distribution": resolved.python_distribution,
        "python_package": resolved.python_package,
        "default_repo_pack": False,
        "notes": f"Hosted-pack registry entry for {resolved.pack_slug}.",
    }


def _pack_root_readme(resolved: _ResolvedPackScaffold) -> str:
    return "\n".join(
        (
            f"# `{resolved.pack_root}`",
            "",
            "## Description",
            (
                f"`Hosted domain-pack root for {resolved.pack_slug}. This starter owns the "
                "pack-local machine state, docs, workflows, tracking surfaces, and Python "
                "runtime that integrate with reusable core through the shared host contract.`"
            ),
            "",
            "## Paths",
            "| Path | Description |",
            "|---|---|",
            (
                f"| `{resolved.pack_root}/README.md` | Describes the hosted-pack root "
                "and its main boundaries. |"
            ),
            (
                f"| `{resolved.pack_root}/.wt/` | Pack-local machine state, manifests, "
                "registries, and starter schemas or artifacts. |"
            ),
            (
                f"| `{resolved.pack_root}/docs/` | Pack-owned durable guidance and "
                "namespace command docs. |"
            ),
            (
                f"| `{resolved.pack_root}/workflows/` | Pack-owned workflow guidance "
                "and routing surfaces. |"
            ),
            (f"| `{resolved.pack_root}/tracking/` | Pack-owned rendered tracking surfaces. |"),
            (
                f"| `{resolved.pack_root}/python/` | Pack-native Python package and "
                "editable-install metadata. |"
            ),
            "",
            "## Boundaries",
            (
                "`Keep generic helpers in watchtower_core, host composition in watchtower_host, "
                "and pack-native behavior in this root. Do not place prose or Python source "
                "under .wt/.`"
            ),
            "",
            "## Notes",
            (
                "`Use watchtower-core pack scaffold output plus the generated registry and "
                "workspace snippets before wiring this pack into shared host composition.`"
            ),
        )
    )


def _docs_readme(resolved: _ResolvedPackScaffold) -> str:
    return "\n".join(
        (
            f"# `{resolved.pack_root}/docs`",
            "",
            "## Description",
            (
                f"`Durable {resolved.pack_slug} guidance root. Keep pack-specific command docs, "
                "operator guidance, and domain standards here rather than in shared core docs.`"
            ),
            "",
            "## Files",
            "| Path | Description |",
            "|---|---|",
            f"| `{resolved.pack_root}/docs/README.md` | Describes the pack-owned docs root. |",
            (
                f"| `{resolved.pack_root}/docs/commands/core_python/"
                f"watchtower_core_{resolved.command_namespace.replace('-', '_')}.md` | "
                "Namespace entry page for the hosted-pack command surface. |"
            ),
        )
    )


def _workflows_readme(resolved: _ResolvedPackScaffold) -> str:
    return "\n".join(
        (
            f"# `{resolved.pack_root}/workflows`",
            "",
            "## Description",
            (
                f"`Workflow guidance root for {resolved.pack_slug}. Keep pack-local routing "
                "and modules here only when the pack owns domain-specific procedures beyond "
                "the shared core workflows.`"
            ),
            "",
            "## Files",
            "| Path | Description |",
            "|---|---|",
            (
                f"| `{resolved.pack_root}/workflows/README.md` | Describes the "
                "pack-local workflow root. |"
            ),
            (
                f"| `{resolved.pack_root}/workflows/ROUTING_TABLE.md` | Starter routing "
                "guidance for future pack-local modules. |"
            ),
        )
    )


def _workflow_routing_table(resolved: _ResolvedPackScaffold) -> str:
    return "\n".join(
        (
            "# Routing Table",
            "",
            (
                f"Use this table when `{resolved.pack_slug}` later adds pack-local workflow "
                "modules. Until then, route shared pack-boundary and validation work through "
                "`core/workflows/ROUTING_TABLE.md`."
            ),
            "",
            "| Task Type | Trigger Keywords (Examples) | Required Workflows |",
            "|---|---|---|",
            (
                f"| {resolved.pack_title} pack integration | {resolved.pack_slug}, pack, "
                "contract, validation | `core/workflows/modules/core.md`, "
                "`core/workflows/modules/domain_pack_integration.md`, "
                "`core/workflows/modules/pack_interface_validation.md` |"
            ),
        )
    )


def _tracking_readme(resolved: _ResolvedPackScaffold) -> str:
    return "\n".join(
        (
            f"# `{resolved.pack_root}/tracking`",
            "",
            "## Description",
            (
                f"`Rendered tracking surfaces for {resolved.pack_slug}. Keep human-facing "
                "tracking views here when the pack owns them.`"
            ),
            "",
            "## Files",
            "| Path | Description |",
            "|---|---|",
            (
                f"| `{resolved.pack_root}/tracking/README.md` | Describes the pack-owned "
                "tracking root. |"
            ),
        )
    )


def _python_readme(resolved: _ResolvedPackScaffold) -> str:
    return "\n".join(
        (
            f"# `watchtower-{resolved.pack_slug}`",
            "",
            (
                f"{resolved.pack_title} pack-native Python runtime. This package owns the "
                f"`watchtower_{resolved.pack_slug.replace('-', '_')}` integration surface and "
                "depends on `watchtower-core` for reusable contracts."
            ),
        )
    )


def _namespace_command_reference(resolved: _ResolvedPackScaffold) -> str:
    return "\n".join(
        (
            f"# `watchtower-core {resolved.command_namespace}`",
            "",
            "## Summary",
            (f"Starter namespace entry page for the hosted `{resolved.pack_slug}` pack."),
            "",
            "## Use When",
            (
                f"- You are adding or evolving `{resolved.pack_slug}` as a hosted pack "
                "under the shared core-host-pack contract."
            ),
            (
                f"- You want the pack-owned command-doc entry page that `watchtower-core "
                f"pack validate` requires for `{resolved.command_namespace}`."
            ),
            "",
            "## Command",
            "| Field | Value |",
            "|---|---|",
            f"| Invocation | `watchtower-core {resolved.command_namespace}` |",
            "| Kind | `pack_namespace` |",
            f"| Workspace | `{resolved.pack_root}/python` |",
            (
                "| Source Surface | "
                f"`{resolved.pack_root}/python/src/{resolved.python_package}/integration.py` |"
            ),
            "",
            "## Synopsis",
            "```sh",
            f"watchtower-core {resolved.command_namespace} <subcommand> [args]",
            "```",
            "",
            "## Arguments and Options",
            (
                "- `<subcommand>`: Replace the starter command groups with pack-owned "
                "runtime commands as the pack grows."
            ),
            "- `-h`, `--help`: Show the command help text.",
            "",
            "## Examples",
            "```sh",
            f"uv run watchtower-core {resolved.command_namespace} --help",
            "```",
            "",
            "## Behavior and Outputs",
            (
                f"- This namespace is registered through "
                f"`{resolved.python_package}.integration.PACK_INTEGRATION`."
            ),
            (
                f"- Keep future `{resolved.command_namespace}` command pages under "
                f"`{resolved.pack_root}/docs/commands/core_python/`."
            ),
            "",
            "## Related Commands",
            "| Command | Relationship |",
            "|---|---|",
            (
                f"| `watchtower-core pack validate --pack-settings-path "
                f"{resolved.pack_settings_path} --format json` | "
                "Validates the pack contract after host wiring is in place. |"
            ),
            (
                f"| `watchtower-core pack describe --pack {resolved.pack_slug} --format json` | "
                "Shows the shared registry entry after the pack is registered. |"
            ),
            "",
            "## Source Surface",
            f"- `{resolved.pack_root}/python/src/{resolved.python_package}/integration.py`",
            f"- `{resolved.pack_settings_path}`",
            f"- `{resolved.pack_runtime_manifest_path}`",
            "",
            "## Updated At",
            f"- `{resolved.updated_at}`",
        )
    )


def _domain_root_readme(
    resolved: _ResolvedPackScaffold,
    root_name: str,
    relative_root: str,
) -> str:
    return "\n".join(
        (
            f"# `{relative_root}`",
            "",
            "## Description",
            (
                f"`Pack-owned {root_name} root for {resolved.pack_slug}. Keep only "
                f"{resolved.pack_slug}-native {root_name} artifacts here.`"
            ),
        )
    )


__all__ = [
    "PackScaffoldRequest",
    "PackScaffoldResult",
    "scaffold_hosted_pack",
]
