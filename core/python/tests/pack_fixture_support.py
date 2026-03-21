from __future__ import annotations

import json
from pathlib import Path
from shutil import copy2, copytree

from watchtower_core.pack_integration import pack_command_entry_doc_path

REPO_ROOT = Path(__file__).resolve().parents[3]
_PLAN_FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "packs" / "plan"
_DEFAULT_FIXTURE_PACK_ROOT = "packs/plan"
_DEFAULT_FIXTURE_WT_ROOT = "packs/plan/.wt"


def materialize_pack_validation_suite(
    pack_root: Path,
    *,
    pack_id: str = "pack.plan",
    pack_slug: str = "plan",
    command_namespace: str = "plan",
    python_distribution: str = "watchtower-plan",
    python_package: str = "watchtower_plan",
    integration_module: str = "watchtower_plan.integration",
    default_repo_pack: bool | None = None,
    include_validation_suite_registry: bool = True,
    suite_step_validator_id: str | None = None,
    validator_schema_ids: tuple[str, ...] | None = None,
    registry_mode: str = "replace_default",
) -> dict[str, str]:
    repo_root = _discover_repo_root(pack_root)
    copytree(_PLAN_FIXTURE_ROOT, pack_root, dirs_exist_ok=True)

    actual_wt_root = f"{pack_root.relative_to(repo_root).as_posix()}/.wt"
    actual_pack_root = actual_wt_root.removesuffix("/.wt")
    note_slug = f"{pack_slug}_note"
    schema_slug = f"{pack_slug}-note"
    suite_id = f"suite.{pack_slug}.validation_baseline"
    validator_id = f"validator.packs.{note_slug}"
    schema_id = f"urn:watchtower:schema:interfaces:packs:{schema_slug}:v1"

    if note_slug != "plan_note":
        original_artifact_path = pack_root / ".wt" / "work_items" / "plan_note.json"
        renamed_artifact_path = pack_root / ".wt" / "work_items" / f"{note_slug}.json"
        if original_artifact_path.exists():
            original_artifact_path.rename(renamed_artifact_path)
        original_schema_path = (
            pack_root / ".wt" / "schemas" / "interfaces" / "packs" / "plan_note.schema.json"
        )
        renamed_schema_path = (
            pack_root / ".wt" / "schemas" / "interfaces" / "packs" / f"{note_slug}.schema.json"
        )
        if original_schema_path.exists():
            original_schema_path.rename(renamed_schema_path)

    replacements = (
        (_DEFAULT_FIXTURE_WT_ROOT, actual_wt_root),
        (_DEFAULT_FIXTURE_PACK_ROOT, actual_pack_root),
        ("pack.plan", pack_id),
        ("suite.plan.validation_baseline", suite_id),
        ("validator.packs.plan_note", validator_id),
        ("urn:watchtower:schema:interfaces:packs:plan-note:v1", schema_id),
        ("plan_note", note_slug),
        ("watchtower-plan", python_distribution),
        ("watchtower_plan", python_package),
        ("watchtower_plan.integration", integration_module),
        ('"pack_slug": "plan"', f'"pack_slug": "{pack_slug}"'),
        ('"command_namespace": "plan"', f'"command_namespace": "{command_namespace}"'),
    )
    for path in sorted(pack_root.rglob("*.json")):
        text = path.read_text(encoding="utf-8")
        for old, new in replacements:
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")

    runtime_manifest = _load_json(pack_root / ".wt/manifests/pack_runtime_manifest.json")
    _materialize_owned_roots(repo_root, runtime_manifest["owned_roots"])
    command_doc_relative_path = pack_command_entry_doc_path(
        command_namespace=command_namespace,
        docs_root=runtime_manifest["owned_roots"]["docs_root"],
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
                "## Updated At",
                "- `2026-03-21T02:20:00Z`",
                "",
            )
        ),
        encoding="utf-8",
    )

    pack_registry_path = repo_root / "core" / "control_plane" / "registries" / "pack_registry.json"
    if pack_registry_path.exists():
        pack_registry = _load_json(pack_registry_path)
        effective_default_pack = (
            default_repo_pack if default_repo_pack is not None else (pack_slug == "plan")
        )
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
            updated: list[dict[str, object]] = []
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

    if validator_schema_ids is not None:
        validator_registry = _load_json(pack_root / ".wt/registries/validator_registry.json")
        for validator in validator_registry["validators"]:
            if validator["id"] == _PLAN_NOTE_VALIDATOR_ID:
                validator["schema_ids"] = list(validator_schema_ids)
                break
        _write_json(pack_root / ".wt/registries/validator_registry.json", validator_registry)

    return {
        "artifact_relative_path": f"{actual_wt_root}/work_items/{note_slug}.json",
        "command_doc_relative_path": command_doc_relative_path,
        "pack_settings_path": f"{actual_wt_root}/manifests/pack_settings.json",
        "pack_runtime_manifest_path": f"{actual_wt_root}/manifests/pack_runtime_manifest.json",
        "schema_id": schema_id,
        "schema_relative_path": f"{actual_wt_root}/schemas/interfaces/packs/{note_slug}.schema.json",
        "suite_id": suite_id,
        "validation_suite_registry_path": validation_suite_registry_path,
        "validator_id": validator_id,
    }


def materialize_validation_repo_subset(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


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


def _discover_repo_root(start: Path) -> Path:
    candidate = start.resolve()
    for parent in (candidate, *candidate.parents):
        if (parent / "core/control_plane").is_dir() and (parent / "core/python").is_dir():
            return parent
    raise ValueError(f"Could not discover repo root for fixture destination: {start}")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, document: dict[str, object]) -> None:
    path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def _materialize_owned_roots(repo_root: Path, owned_roots: dict[str, object]) -> None:
    for relative_path in owned_roots.values():
        if not isinstance(relative_path, str) or not relative_path:
            continue
        (repo_root / relative_path).mkdir(parents=True, exist_ok=True)
