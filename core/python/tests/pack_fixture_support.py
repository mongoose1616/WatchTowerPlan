from __future__ import annotations

import json
import subprocess
from pathlib import Path
from shutil import copy2, copytree, ignore_patterns
from typing import Any, cast

from watchtower_core.pack_integration.docs import pack_command_entry_doc_path
from watchtower_core.pack_integration.workspace_registration import (
    core_python_workspace_registration,
    ensure_core_python_workspace_registration,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
_FIXTURE_TEMPLATE_ROOT = Path(__file__).resolve().parent / "fixtures" / "packs" / "fixture"
_DEFAULT_FIXTURE_PACK_ROOT = "packs/fixture"
_DEFAULT_FIXTURE_WT_ROOT = "packs/fixture/.wt"
_DEFAULT_PACK_ID = "pack.fixture"
_DEFAULT_PACK_SLUG = "fixture"
_DEFAULT_COMMAND_NAMESPACE = "fixture"
_DEFAULT_PYTHON_DISTRIBUTION = "watchtower-fixture-pack"
_DEFAULT_PYTHON_PACKAGE = "watchtower_fixture_pack"
_DEFAULT_INTEGRATION_MODULE = "watchtower_fixture_pack.integration"


def materialize_pack_validation_suite(
    pack_root: Path,
    *,
    pack_id: str = _DEFAULT_PACK_ID,
    pack_slug: str = _DEFAULT_PACK_SLUG,
    command_namespace: str = _DEFAULT_COMMAND_NAMESPACE,
    python_distribution: str = _DEFAULT_PYTHON_DISTRIBUTION,
    python_package: str = _DEFAULT_PYTHON_PACKAGE,
    integration_module: str = _DEFAULT_INTEGRATION_MODULE,
    default_repo_pack: bool | None = None,
    include_validation_suite_registry: bool = True,
    suite_step_validator_id: str | None = None,
    validator_schema_ids: tuple[str, ...] | None = None,
    registry_mode: str = "replace_default",
    extra_domain_root_names: tuple[str, ...] = (),
    register_with_host_registry: bool = True,
    register_with_core_python_workspace: bool = True,
) -> dict[str, str]:
    repo_root = _discover_repo_root(pack_root)
    inferred_pack_slug = pack_root.name
    if pack_slug == _DEFAULT_PACK_SLUG:
        pack_slug = inferred_pack_slug
    if pack_id == _DEFAULT_PACK_ID:
        pack_id = f"pack.{pack_slug}"
    if command_namespace == _DEFAULT_COMMAND_NAMESPACE:
        command_namespace = pack_slug
    if python_distribution == _DEFAULT_PYTHON_DISTRIBUTION:
        python_distribution = f"watchtower-{pack_slug}-fixture"
    if python_package == _DEFAULT_PYTHON_PACKAGE:
        python_package = f"watchtower_{pack_slug}_fixture"
    if integration_module == _DEFAULT_INTEGRATION_MODULE:
        integration_module = f"{python_package}.integration"
    copytree(_FIXTURE_TEMPLATE_ROOT, pack_root, dirs_exist_ok=True)

    actual_wt_root = f"{pack_root.relative_to(repo_root).as_posix()}/.wt"
    actual_pack_root = actual_wt_root.removesuffix("/.wt")
    note_slug = f"{pack_slug}_note"
    schema_slug = f"{pack_slug}-note"
    suite_id = f"suite.{pack_slug}.validation_baseline"
    validator_id = f"validator.packs.{note_slug}"
    schema_id = f"urn:watchtower:schema:interfaces:packs:{schema_slug}:v1"
    _materialize_synthetic_pack_python(
        pack_root=pack_root,
        pack_id=pack_id,
        pack_slug=pack_slug,
        command_namespace=command_namespace,
        python_distribution=python_distribution,
        python_package=python_package,
    )

    if note_slug != "fixture_note":
        original_artifact_path = pack_root / ".wt" / "work_items" / "fixture_note.json"
        renamed_artifact_path = pack_root / ".wt" / "work_items" / f"{note_slug}.json"
        if original_artifact_path.exists():
            original_artifact_path.rename(renamed_artifact_path)
        original_schema_path = (
            pack_root / ".wt" / "schemas" / "interfaces" / "packs" / "fixture_note.schema.json"
        )
        renamed_schema_path = (
            pack_root / ".wt" / "schemas" / "interfaces" / "packs" / f"{note_slug}.schema.json"
        )
        if original_schema_path.exists():
            original_schema_path.rename(renamed_schema_path)

    replacements = (
        (_DEFAULT_FIXTURE_WT_ROOT, actual_wt_root),
        (_DEFAULT_FIXTURE_PACK_ROOT, actual_pack_root),
        ("pack.fixture", pack_id),
        ("suite.fixture.validation_baseline", suite_id),
        ("validator.packs.fixture_note", validator_id),
        ("validator.fixture.pack_runtime_manifest", f"validator.{pack_slug}.pack_runtime_manifest"),
        ("urn:watchtower:schema:interfaces:packs:fixture-note:v1", schema_id),
        ("fixture_note", note_slug),
        ("watchtower-fixture-pack", python_distribution),
        ("watchtower_fixture_pack", python_package),
        ("watchtower_fixture_pack.integration", integration_module),
        ('"pack_slug": "fixture"', f'"pack_slug": "{pack_slug}"'),
        ('"command_namespace": "fixture"', f'"command_namespace": "{command_namespace}"'),
    )
    for path in sorted(pack_root.rglob("*.json")):
        text = path.read_text(encoding="utf-8")
        for old, new in replacements:
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")

    if not actual_pack_root.startswith("packs/"):
        schema_catalog_path = pack_root / ".wt" / "registries" / "schema_catalog.json"
        if schema_catalog_path.exists():
            schema_catalog = _load_json(schema_catalog_path)
            for record in schema_catalog.get("schemas", []):
                canonical_path = record.get("canonical_path")
                if not isinstance(canonical_path, str):
                    continue
                misplaced_prefix = f"{actual_wt_root}/schemas/interfaces/"
                if not canonical_path.startswith(misplaced_prefix):
                    continue
                if canonical_path.startswith(f"{actual_wt_root}/schemas/interfaces/packs/"):
                    continue
                filename = canonical_path.rsplit("/", maxsplit=1)[-1]
                record["canonical_path"] = (
                    f"{actual_wt_root}/schemas/interfaces/packs/{filename}"
                )
            _write_json(schema_catalog_path, schema_catalog)

    runtime_manifest = _load_json(pack_root / ".wt/manifests/pack_runtime_manifest.json")
    pack_settings = _load_json(pack_root / ".wt/manifests/pack_settings.json")
    if extra_domain_root_names:
        extra_domain_roots = {
            root_name: f"{actual_pack_root}/{root_name}" for root_name in extra_domain_root_names
        }
        pack_settings["workspace_roots"].setdefault("domain_roots", {}).update(extra_domain_roots)
        runtime_manifest["owned_roots"].setdefault("domain_roots", {}).update(extra_domain_roots)
        _write_json(pack_root / ".wt/manifests/pack_settings.json", pack_settings)
        _write_json(pack_root / ".wt/manifests/pack_runtime_manifest.json", runtime_manifest)
    _materialize_owned_roots(repo_root, runtime_manifest["owned_roots"])
    command_doc_relative_path = pack_command_entry_doc_path(
        command_namespace=command_namespace,
        docs_root=runtime_manifest["owned_roots"]["docs_root"],
    )
    command_source_surface = (
        f"{actual_pack_root}/python/src/{integration_module.replace('.', '/')}.py"
    )
    command_doc_path = repo_root / command_doc_relative_path
    command_doc_path.parent.mkdir(parents=True, exist_ok=True)
    command_doc_path.write_text(
        "\n".join(
            (
                f"# `watchtower-core {command_namespace}`",
                "",
                "## Summary",
                f"Fixture command page for the `{command_namespace}` hosted-pack namespace.",
                "",
                "## Command",
                "| Field | Value |",
                "|---|---|",
                f"| Invocation | `watchtower-core {command_namespace}` |",
                "| Kind | `root_command` |",
                "| Workspace | `core_python` |",
                f"| Source Surface | `{command_source_surface}` |",
                "",
                "## Source Surface",
                f"- `{command_source_surface}`",
                "",
                "## Updated At",
                "- `2026-03-21T02:20:00Z`",
                "",
            )
        ),
        encoding="utf-8",
    )
    sync_command_doc_path = (
        repo_root
        / runtime_manifest["owned_roots"]["docs_root"]
        / "commands"
        / "core_python"
        / f"watchtower_core_{command_namespace}_sync.md"
    )
    sync_command_doc_path.parent.mkdir(parents=True, exist_ok=True)
    sync_command_doc_path.write_text(
        "\n".join(
            (
                f"# `watchtower-core {command_namespace} sync`",
                "",
                "## Summary",
                f"Fixture command page for the `{command_namespace} sync` hosted-pack family.",
                "",
                "## Command",
                "| Field | Value |",
                "|---|---|",
                f"| Invocation | `watchtower-core {command_namespace} sync` |",
                "| Kind | `subcommand_family` |",
                "| Workspace | `core_python` |",
                f"| Source Surface | `{command_source_surface}` |",
                "",
                "## Source Surface",
                f"- `{command_source_surface}`",
                "",
                "## Updated At",
                "- `2026-03-29T02:10:00Z`",
                "",
            )
        ),
        encoding="utf-8",
    )
    sync_all_command_doc_path = (
        repo_root
        / runtime_manifest["owned_roots"]["docs_root"]
        / "commands"
        / "core_python"
        / f"watchtower_core_{command_namespace}_sync_all.md"
    )
    sync_all_command_doc_path.parent.mkdir(parents=True, exist_ok=True)
    sync_all_command_doc_path.write_text(
        "\n".join(
            (
                f"# `watchtower-core {command_namespace} sync all`",
                "",
                "## Summary",
                f"Fixture command page for the `{command_namespace} sync all` hosted-pack command.",
                "",
                "## Command",
                "| Field | Value |",
                "|---|---|",
                f"| Invocation | `watchtower-core {command_namespace} sync all` |",
                "| Kind | `subcommand` |",
                "| Workspace | `core_python` |",
                f"| Source Surface | `{command_source_surface}` |",
                "",
                "## Source Surface",
                f"- `{command_source_surface}`",
                "",
                "## Updated At",
                "- `2026-03-29T02:12:00Z`",
                "",
            )
        ),
        encoding="utf-8",
    )

    pack_registry_path = repo_root / "core" / "control_plane" / "registries" / "pack_registry.json"
    if register_with_host_registry and pack_registry_path.exists():
        pack_registry = _load_json(pack_registry_path)
        effective_default_pack = default_repo_pack if default_repo_pack is not None else False
        registry_entry = {
            "pack_id": pack_id,
            "pack_slug": pack_slug,
            "command_namespace": command_namespace,
            "pack_settings_path": f"{actual_wt_root}/manifests/pack_settings.json",
            "pack_runtime_manifest_path": f"{actual_wt_root}/manifests/pack_runtime_manifest.json",
            "python_distribution": python_distribution,
            "python_package": python_package,
            "default_repo_pack": effective_default_pack,
            "notes": (
                f"The {pack_slug} pack fixture exercises hosted-pack integration "
                "without changing reusable-core runtime code."
            ),
        }
        packs = list(pack_registry["packs"])
        if registry_mode == "append":
            packs = [
                entry
                for entry in packs
                if entry["pack_id"] != pack_id and entry["pack_slug"] != pack_slug
            ]
            packs.append(registry_entry)
        elif registry_mode == "replace_default":
            replaced = False
            updated: list[dict[str, Any]] = []
            for entry in packs:
                if entry.get("pack_id") == pack_id or entry.get("default_repo_pack") is True:
                    updated.append(registry_entry)
                    replaced = True
                else:
                    updated.append(entry)
            packs = updated if replaced else [*updated, registry_entry]
        else:
            raise ValueError(f"Unknown registry_mode: {registry_mode}")
        pack_registry["packs"] = packs
        _write_json(pack_registry_path, pack_registry)

    pyproject_path = repo_root / "core" / "python" / "pyproject.toml"
    if register_with_core_python_workspace and pyproject_path.exists():
        ensure_core_python_workspace_registration(
            pyproject_path,
            core_python_workspace_registration(
                repo_root,
                python_root=f"{actual_pack_root}/python",
                python_distribution=python_distribution,
            ),
        )

    validation_suite_registry_path = f"{actual_wt_root}/registries/validation_suite_registry.json"
    if not include_validation_suite_registry:
        suite_registry_file = pack_root / ".wt/registries/validation_suite_registry.json"
        if suite_registry_file.exists():
            suite_registry_file.unlink()
        pack_settings = _load_json(pack_root / ".wt/manifests/pack_settings.json")
        pack_settings["surfaces"] = [
            surface
            for surface in pack_settings["surfaces"]
            if surface["surface_name"] != "validation_suite_registry"
        ]
        _write_json(pack_root / ".wt/manifests/pack_settings.json", pack_settings)
    elif suite_step_validator_id is not None:
        suite_registry = _load_json(pack_root / ".wt/registries/validation_suite_registry.json")
        suite_registry["suites"][0]["steps"][1]["validator_id"] = suite_step_validator_id
        _write_json(pack_root / ".wt/registries/validation_suite_registry.json", suite_registry)

    validator_registry_path = pack_root / ".wt/registries/validator_registry.json"
    if validator_registry_path.exists():
        validator_registry = _load_json(validator_registry_path)
        core_validator_registry = _load_json(
            repo_root / "core" / "control_plane" / "registries" / "validator_registry.json"
        )
        core_validator_ids = {
            validator["id"] for validator in core_validator_registry["validators"]
        }
        validator_registry["validators"] = [
            validator
            for validator in validator_registry["validators"]
            if validator["id"] not in core_validator_ids
        ]
        _write_json(validator_registry_path, validator_registry)

    if validator_schema_ids is not None:
        validator_registry = _load_json(validator_registry_path)
        for validator in validator_registry["validators"]:
            if validator["id"] == validator_id:
                validator["schema_ids"] = list(validator_schema_ids)
                break
        _write_json(validator_registry_path, validator_registry)

    return {
        "artifact_relative_path": f"{actual_wt_root}/work_items/{note_slug}.json",
        "command_doc_relative_path": command_doc_relative_path,
        "pack_settings_path": f"{actual_wt_root}/manifests/pack_settings.json",
        "pack_runtime_manifest_path": f"{actual_wt_root}/manifests/pack_runtime_manifest.json",
        "schema_id": schema_id,
        "schema_relative_path": (
            f"{actual_wt_root}/schemas/interfaces/packs/{note_slug}.schema.json"
        ),
        "suite_id": suite_id,
        "validation_suite_registry_path": validation_suite_registry_path,
        "validator_id": validator_id,
    }


def materialize_pack_task_index_surface(
    pack_root: Path,
    *,
    pack_slug: str | None = None,
) -> dict[str, str]:
    """Add one pack-owned task index backed by a pack-local schema."""

    repo_root = _discover_repo_root(pack_root)
    actual_pack_root = pack_root.relative_to(repo_root).as_posix()
    actual_wt_root = f"{actual_pack_root}/.wt"
    effective_pack_slug = pack_slug or pack_root.name
    schema_id = f"urn:watchtower:schema:artifacts:{effective_pack_slug}:task-summary-index:v1"
    schema_relative_path = f"{actual_wt_root}/schemas/artifacts/task_index.schema.json"
    task_index_relative_path = f"{actual_wt_root}/indexes/task_index.json"
    task_index_id = f"index.{effective_pack_slug}_tasks"
    (repo_root / schema_relative_path).parent.mkdir(parents=True, exist_ok=True)
    (repo_root / task_index_relative_path).parent.mkdir(parents=True, exist_ok=True)
    _write_json(
        repo_root / schema_relative_path,
        {
            "$id": schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": f"{effective_pack_slug.title()} Task Index",
            "description": "Pack-local task index schema for copied-core fixture tests.",
            "type": "object",
            "required": ["$schema", "id", "title", "status", "entries"],
            "properties": {
                "$schema": {"const": schema_id},
                "id": {"const": task_index_id},
                "title": {"type": "string", "minLength": 1},
                "status": {"type": "string", "enum": ["draft", "active", "deprecated"]},
                "entries": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": [
                            "task_id",
                            "initiative_id",
                            "trace_id",
                            "initiative_title",
                            "title",
                            "summary",
                            "status",
                            "task_status",
                            "task_kind",
                            "priority",
                            "owner",
                            "doc_path",
                            "updated_at",
                        ],
                        "properties": {
                            "task_id": {"type": "string", "minLength": 1},
                            "initiative_id": {"type": "string", "minLength": 1},
                            "trace_id": {"type": "string", "minLength": 1},
                            "initiative_title": {"type": "string", "minLength": 1},
                            "title": {"type": "string", "minLength": 1},
                            "summary": {"type": "string", "minLength": 1},
                            "status": {
                                "type": "string",
                                "enum": ["draft", "active", "deprecated"],
                            },
                            "task_status": {
                                "type": "string",
                                "enum": [
                                    "planned",
                                    "ready",
                                    "in_progress",
                                    "in_review",
                                    "blocked",
                                    "completed",
                                    "cancelled",
                                ],
                            },
                            "task_kind": {"type": "string", "minLength": 1},
                            "priority": {
                                "type": "string",
                                "enum": ["critical", "high", "medium", "low"],
                            },
                            "owner": {"type": "string", "minLength": 1},
                            "doc_path": {"type": "string", "minLength": 1},
                            "updated_at": {"type": "string", "format": "date-time"},
                        },
                        "additionalProperties": False,
                    },
                },
            },
            "additionalProperties": False,
        },
    )
    _write_json(
        repo_root / task_index_relative_path,
        {
            "$schema": schema_id,
            "id": task_index_id,
            "title": f"{effective_pack_slug.title()} Task Index",
            "status": "active",
            "entries": [
                {
                    "task_id": f"task.{effective_pack_slug}.bootstrap",
                    "initiative_id": f"initiative.{effective_pack_slug}_bootstrap",
                    "trace_id": f"trace.{effective_pack_slug}_bootstrap",
                    "initiative_title": f"{effective_pack_slug.title()} Bootstrap",
                    "title": f"Bootstrap {effective_pack_slug}",
                    "summary": f"Bootstrap the {effective_pack_slug} fixture pack.",
                    "status": "active",
                    "task_status": "ready",
                    "task_kind": "governance",
                    "priority": "high",
                    "owner": "repository_maintainer",
                    "doc_path": f"{actual_wt_root}/tasks/bootstrap/task.json",
                    "updated_at": "2026-03-23T20:15:00Z",
                }
            ],
        },
    )
    schema_catalog_path = pack_root / ".wt" / "registries" / "schema_catalog.json"
    schema_catalog = _load_json(schema_catalog_path)
    schema_catalog.setdefault("schemas", []).append(
        {
            "schema_id": schema_id,
            "title": f"{effective_pack_slug.title()} Task Index",
            "description": "Pack-local task index schema for copied-core fixture tests.",
            "status": "active",
            "schema_family": "artifact",
            "subject_kind": "task_index",
            "version": "v1",
            "canonical_path": schema_relative_path,
        }
    )
    _write_json(schema_catalog_path, schema_catalog)
    pack_settings_path = pack_root / ".wt" / "manifests" / "pack_settings.json"
    pack_settings = _load_json(pack_settings_path)
    pack_settings.setdefault("surfaces", []).append(
        {
            "surface_name": "task_index",
            "surface_kind": "index",
            "path": task_index_relative_path,
            "authority": "derived",
            "visibility": "mixed",
            "rebuildable": True,
        }
    )
    _write_json(pack_settings_path, pack_settings)
    return {
        "schema_id": schema_id,
        "schema_relative_path": schema_relative_path,
        "task_index_path": task_index_relative_path,
    }


def materialize_validation_repo_subset(
    tmp_path: Path,
    *,
    include_shared_discovery_sources: bool = False,
) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    copytree(
        REPO_ROOT / "core" / "docs" / "commands",
        repo_root / "core" / "docs" / "commands",
    )
    copytree(
        REPO_ROOT / "core" / "docs" / "templates",
        repo_root / "core" / "docs" / "templates",
    )
    (repo_root / "core" / "python").mkdir(parents=True)
    copy2(
        REPO_ROOT / "core" / "python" / "pyproject.toml",
        repo_root / "core" / "python" / "pyproject.toml",
    )
    copytree(
        REPO_ROOT / "core" / "python" / "src" / "watchtower_host",
        repo_root / "core" / "python" / "src" / "watchtower_host",
    )
    if include_shared_discovery_sources:
        if not _copy_git_tracked_tree(REPO_ROOT, repo_root, "core"):
            copytree(
                REPO_ROOT / "core",
                repo_root / "core",
                dirs_exist_ok=True,
                ignore=ignore_patterns(
                    ".venv",
                    "__pycache__",
                    ".pytest_cache",
                    ".ruff_cache",
                    ".mypy_cache",
                ),
            )
            for source_path in REPO_ROOT.iterdir():
                if not source_path.is_file():
                    continue
                copy2(source_path, repo_root / source_path.name)
            github_root = REPO_ROOT / ".github"
            if github_root.exists():
                copytree(github_root, repo_root / ".github", dirs_exist_ok=True)
            githooks_root = REPO_ROOT / ".githooks"
            if githooks_root.exists():
                copytree(githooks_root, repo_root / ".githooks", dirs_exist_ok=True)
        else:
            _copy_git_tracked_root_files(REPO_ROOT, repo_root)
            _copy_git_tracked_tree(REPO_ROOT, repo_root, ".github")
            if not _copy_git_tracked_tree(REPO_ROOT, repo_root, ".githooks"):
                githooks_root = REPO_ROOT / ".githooks"
                if githooks_root.exists():
                    copytree(githooks_root, repo_root / ".githooks", dirs_exist_ok=True)
    return repo_root


def _copy_git_tracked_root_files(source_root: Path, destination_root: Path) -> None:
    tracked_paths = _git_tracked_relative_paths(source_root, ".")
    if tracked_paths is None:
        return
    for tracked_path in tracked_paths:
        source_path = source_root / tracked_path
        if not source_path.is_file() or "/" in tracked_path:
            continue
        destination = destination_root / tracked_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        copy2(source_path, destination)


def _copy_git_tracked_tree(
    source_root: Path,
    destination_root: Path,
    relative_path: str,
) -> bool:
    tracked_paths = _git_tracked_relative_paths(source_root, relative_path)
    if not tracked_paths:
        return False

    (destination_root / relative_path).mkdir(parents=True, exist_ok=True)
    for tracked_path in tracked_paths:
        source_path = source_root / tracked_path
        if not source_path.is_file():
            continue
        destination = destination_root / tracked_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        copy2(source_path, destination)
    return True


def _git_tracked_relative_paths(
    repo_root: Path,
    relative_path: str,
) -> tuple[str, ...] | None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return None
    if completed.returncode != 0:
        return None

    listed = subprocess.run(
        ["git", "-C", str(repo_root), "ls-files", "-z", "--", relative_path],
        check=False,
        capture_output=True,
        text=True,
    )
    if listed.returncode != 0:
        return None
    return tuple(path for path in listed.stdout.split("\0") if path)


def materialize_externalized_fixture_python(
    pack_python_root: Path,
    *,
    python_distribution: str,
    python_package: str,
    source_package_root: Path,
    description: str,
) -> None:
    """Materialize a synthetic pack package under one pack-owned python root."""

    repo_root = _discover_repo_root(pack_python_root)
    actual_pack_root = pack_python_root.relative_to(repo_root).as_posix().removesuffix("/python")
    pack_python_root.mkdir(parents=True, exist_ok=True)
    (pack_python_root / "src").mkdir(parents=True, exist_ok=True)
    (pack_python_root / "pyproject.toml").write_text(
        "\n".join(
            (
                "[build-system]",
                'requires = ["hatchling>=1.27"]',
                'build-backend = "hatchling.build"',
                "",
                "[project]",
                f'name = "{python_distribution}"',
                'version = "0.1.0"',
                f'description = "{description}"',
                'readme = "README.md"',
                'requires-python = ">=3.12,<3.13"',
                "dependencies = []",
                "",
                "[tool.hatch.build.targets.wheel]",
                f'packages = ["src/{python_package}"]',
                "",
            )
        ),
        encoding="utf-8",
    )
    (pack_python_root / "README.md").write_text(
        f"# `{python_distribution}`\n\n{description}\n",
        encoding="utf-8",
    )
    copytree(
        source_package_root,
        pack_python_root / "src" / python_package,
        dirs_exist_ok=True,
        ignore=ignore_patterns("__pycache__", "*.pyc"),
    )
    if source_package_root.is_relative_to(REPO_ROOT):
        source_surface_prefix = f"{source_package_root.relative_to(REPO_ROOT).as_posix()}/"
        target_surface_prefix = f"{actual_pack_root}/python/src/{python_package}/"
        for path in sorted((pack_python_root / "src" / python_package).rglob("*.py")):
            text = path.read_text(encoding="utf-8")
            text = text.replace(source_surface_prefix, target_surface_prefix)
            path.write_text(text, encoding="utf-8")


def _materialize_synthetic_pack_python(
    *,
    pack_root: Path,
    pack_id: str,
    pack_slug: str,
    command_namespace: str,
    python_distribution: str,
    python_package: str,
) -> None:
    repo_root = _discover_repo_root(pack_root)
    package_root = pack_root / "python" / "src" / python_package
    if package_root.exists():
        return
    materialize_externalized_fixture_python(
        pack_root / "python",
        python_distribution=python_distribution,
        python_package=python_package,
        source_package_root=(
            REPO_ROOT
            / "core"
            / "python"
            / "tests"
            / "fixtures"
            / "python"
            / "watchtower_oversight_fixture"
        ),
        description=(
            f"Synthetic {pack_slug} runtime package used to prove hosted-pack portability."
        ),
    )
    integration_path = package_root / "integration.py"
    integration_text = integration_path.read_text(encoding="utf-8")
    integration_text = integration_text.replace(
        'pack_id="pack.oversight"',
        f'pack_id="{pack_id}"',
    )
    integration_text = integration_text.replace(
        'pack_slug="oversight"',
        f'pack_slug="{pack_slug}"',
    )
    integration_text = integration_text.replace(
        'command_namespace="oversight"',
        f'command_namespace="{command_namespace}"',
    )
    integration_text = integration_text.replace(
        '        "oversight",',
        f'        "{command_namespace}",',
        1,
    )
    integration_text = integration_text.replace(
        'python_package="watchtower_oversight_fixture"',
        f'python_package="{python_package}"',
    )
    integration_text = integration_text.replace(
        "Synthetic oversight namespace used to prove hosted-pack extensibility.",
        f"Synthetic {command_namespace} namespace used to prove hosted-pack extensibility.",
    )
    integration_text = integration_text.replace(
        '"core/python/tests/fixtures/python/watchtower_oversight_fixture/integration.py"',
        f'"{pack_root.relative_to(repo_root).as_posix()}/python/src/{python_package}/integration.py"',
    )
    integration_path.write_text(integration_text, encoding="utf-8")


def _discover_repo_root(start: Path) -> Path:
    candidate = start.resolve()
    for parent in (candidate, *candidate.parents):
        if (parent / "core/control_plane").is_dir() and (parent / "core/python").is_dir():
            return parent
    raise ValueError(f"Could not discover repo root for fixture destination: {start}")


def _load_json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def _write_json(path: Path, document: dict[str, Any]) -> None:
    path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def _materialize_owned_roots(repo_root: Path, owned_roots: dict[str, Any]) -> None:
    for relative_path in owned_roots.values():
        if isinstance(relative_path, str) and relative_path:
            (repo_root / relative_path).mkdir(parents=True, exist_ok=True)
            continue
        if isinstance(relative_path, dict):
            for nested_relative_path in relative_path.values():
                if isinstance(nested_relative_path, str) and nested_relative_path:
                    (repo_root / nested_relative_path).mkdir(parents=True, exist_ok=True)
