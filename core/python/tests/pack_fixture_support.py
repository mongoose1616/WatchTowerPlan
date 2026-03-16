from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

REPO_ROOT = Path(__file__).resolve().parents[3]
_PLAN_FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "domain_packs" / "plan"
_DEFAULT_FIXTURE_WT_ROOT = "domain_packs/plan/.wt"
_PLAN_NOTE_VALIDATOR_ID = "validator.domain_packs.plan_note"
_PLAN_SUITE_ID = "suite.plan.validation_baseline"


def materialize_pack_validation_suite(
    pack_root: Path,
    *,
    include_validation_suite_registry: bool = True,
    suite_step_validator_id: str | None = None,
    validator_schema_ids: tuple[str, ...] | None = None,
) -> dict[str, str]:
    repo_root = _discover_repo_root(pack_root)
    copytree(_PLAN_FIXTURE_ROOT, pack_root, dirs_exist_ok=True)

    actual_wt_root = f"{pack_root.relative_to(repo_root).as_posix()}/.wt"
    if actual_wt_root != _DEFAULT_FIXTURE_WT_ROOT:
        for relative_path in (
            ".wt/pack_settings.json",
            ".wt/registries/schema_catalog.json",
            ".wt/registries/validator_registry.json",
            ".wt/registries/validation_suite_registry.json",
        ):
            path = pack_root / relative_path
            if not path.exists():
                continue
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    _DEFAULT_FIXTURE_WT_ROOT,
                    actual_wt_root,
                ),
                encoding="utf-8",
            )

    validation_suite_registry_path = f"{actual_wt_root}/registries/validation_suite_registry.json"
    if not include_validation_suite_registry:
        suite_registry_file = pack_root / ".wt/registries/validation_suite_registry.json"
        if suite_registry_file.exists():
            suite_registry_file.unlink()
        pack_settings = _load_json(pack_root / ".wt/pack_settings.json")
        pack_settings["surfaces"] = [
            surface
            for surface in pack_settings["surfaces"]
            if surface["surface_name"] != "validation_suite_registry"
        ]
        _write_json(pack_root / ".wt/pack_settings.json", pack_settings)
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
        "artifact_relative_path": f"{actual_wt_root}/work_items/plan_note.json",
        "pack_settings_path": f"{actual_wt_root}/pack_settings.json",
        "schema_id": "urn:watchtower:schema:interfaces:domain-packs:plan-note:v1",
        "schema_relative_path": f"{actual_wt_root}/schemas/interfaces/domain_packs/plan_note.schema.json",
        "suite_id": _PLAN_SUITE_ID,
        "validation_suite_registry_path": validation_suite_registry_path,
        "validator_id": _PLAN_NOTE_VALIDATOR_ID,
    }


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
