from __future__ import annotations

import re
from pathlib import Path
from shutil import copy2, copytree

from tests.pack_fixture_support import REPO_ROOT, materialize_pack_validation_suite


def externalized_plan_command_surface_paths(pack_root: Path) -> dict[str, str]:
    """Return plan CLI source-surface paths rooted at one externalized pack root."""

    repo_root = _discover_repo_root(pack_root)
    actual_pack_root = pack_root.relative_to(repo_root).as_posix()
    cli_root = f"{actual_pack_root}/python/src/watchtower_plan/cli"
    return {
        "namespace": f"{cli_root}/namespace.py",
        "handlers": f"{cli_root}/handlers.py",
        "query": f"{cli_root}/query.py",
        "sync": f"{cli_root}/sync.py",
        "closeout": f"{cli_root}/closeout.py",
        "tasks": f"{cli_root}/tasks.py",
    }


def materialize_externalized_plan_python(pack_python_root: Path) -> None:
    """Copy the live plan package into an externalized pack-owned python root."""

    source_root = REPO_ROOT / "plan" / "python"
    pack_python_root.mkdir(parents=True, exist_ok=True)
    for filename in ("pyproject.toml", "README.md", "AGENTS.md"):
        source_path = source_root / filename
        if source_path.exists():
            copy2(source_path, pack_python_root / filename)
    copytree(
        source_root / "src" / "watchtower_plan",
        pack_python_root / "src" / "watchtower_plan",
        dirs_exist_ok=True,
    )


def materialize_externalized_plan_validation_suite(
    pack_root: Path,
    *,
    default_repo_pack: bool | None = None,
    include_validation_suite_registry: bool = True,
    suite_step_validator_id: str | None = None,
    validator_schema_ids: tuple[str, ...] | None = None,
    registry_mode: str = "replace_default",
    extra_domain_root_names: tuple[str, ...] = (),
    register_with_host_registry: bool = True,
    register_with_core_python_workspace: bool = True,
) -> dict[str, str]:
    surfaces = materialize_pack_validation_suite(
        pack_root,
        pack_id="pack.plan",
        pack_slug="plan",
        command_namespace="plan",
        python_distribution="watchtower-plan",
        python_package="watchtower_plan",
        integration_module="watchtower_plan.integration",
        default_repo_pack=default_repo_pack,
        include_validation_suite_registry=include_validation_suite_registry,
        suite_step_validator_id=suite_step_validator_id,
        validator_schema_ids=validator_schema_ids,
        registry_mode=registry_mode,
        extra_domain_root_names=extra_domain_root_names,
        register_with_host_registry=register_with_host_registry,
        register_with_core_python_workspace=register_with_core_python_workspace,
    )
    materialize_externalized_plan_python(pack_root / "python")
    return surfaces


def materialize_externalized_plan_command_docs(pack_root: Path) -> None:
    """Copy live plan command docs into one externalized pack root."""

    repo_root = _discover_repo_root(pack_root)
    actual_pack_root = pack_root.relative_to(repo_root).as_posix()
    source_root = REPO_ROOT / "plan" / "docs" / "commands"
    target_root = pack_root / "docs" / "commands"
    copytree(source_root, target_root, dirs_exist_ok=True)
    for path in sorted(target_root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            r"(?<!packs/)(/?)plan/python/src/watchtower_plan/",
            rf"\1{actual_pack_root}/python/src/watchtower_plan/",
            text,
        )
        path.write_text(text, encoding="utf-8")


def _discover_repo_root(start: Path) -> Path:
    candidate = start.resolve()
    for parent in (candidate, *candidate.parents):
        if (parent / "core/control_plane").is_dir() and (parent / "core/python").is_dir():
            return parent
    raise ValueError(f"Could not discover repo root for fixture destination: {start}")
