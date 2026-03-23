from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from shutil import copytree

import pytest

from tests.pack_fixture_support import (
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from tests.unit.control_plane_loader_test_support import REPO_ROOT
from watchtower_core.control_plane.loader import (
    ACCEPTANCE_CONTRACTS_DIRECTORY,
    PACK_REGISTRY_PATH,
    VALIDATOR_REGISTRY_PATH,
    ControlPlaneLoader,
)


def test_control_plane_loader_reuses_validator_registry_materialization(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    validator_registry_path = loader.load_pack_settings().get("validator_registry").path
    validator_registry_loads = 0
    original_load_validated_document = loader.load_validated_document

    def wrapped_load_validated_document(relative_path: str) -> dict[str, object]:
        nonlocal validator_registry_loads
        if relative_path == validator_registry_path:
            validator_registry_loads += 1
        return original_load_validated_document(relative_path)

    monkeypatch.setattr(loader, "load_validated_document", wrapped_load_validated_document)

    first = loader.load_validator_registry()
    second = loader.load_validator_registry()

    assert first is second
    assert validator_registry_loads == 1


def test_control_plane_loader_reuses_pack_registry_materialization(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    pack_registry_loads = 0
    original_load_validated_document = loader.load_validated_document

    def wrapped_load_validated_document(relative_path: str) -> dict[str, object]:
        nonlocal pack_registry_loads
        if relative_path == PACK_REGISTRY_PATH:
            pack_registry_loads += 1
        return original_load_validated_document(relative_path)

    monkeypatch.setattr(loader, "load_validated_document", wrapped_load_validated_document)

    first = loader.load_pack_registry()
    second = loader.load_pack_registry()

    assert first is second
    assert pack_registry_loads == 1


def test_control_plane_loader_invalidates_document_and_directory_cache_state() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    validator_registry_path = loader.load_pack_settings().get("validator_registry").path
    original_registry_document = deepcopy(loader.load_validated_document(validator_registry_path))
    original_contract_documents = tuple(
        (relative_path, deepcopy(document))
        for relative_path, document in loader.iter_validated_documents_with_paths_under(
            ACCEPTANCE_CONTRACTS_DIRECTORY
        )
    )

    original_registry = loader.load_validator_registry()
    stale_registry_document = deepcopy(original_registry_document)
    for validator in stale_registry_document["validators"]:
        if validator["id"] == "validator.plan.validation_bundle":
            validator["title"] = "Stale Plan Validation Bundle Validator"
            break
    else:
        raise AssertionError("Expected plan validator entry to exist in active registry.")
    loader.set_validated_document_override(validator_registry_path, stale_registry_document)

    updated_registry = loader.load_validator_registry()

    assert updated_registry is not original_registry
    assert (
        updated_registry.get("validator.plan.validation_bundle").title
        == "Stale Plan Validation Bundle Validator"
    )

    removed_path, removed_document = original_contract_documents[0]
    stale_directory_documents = (
        (
            removed_path,
            {
                **deepcopy(removed_document),
                "title": "Stale Acceptance Contract Override",
            },
        ),
        *original_contract_documents[1:],
    )
    loader.set_validated_directory_override(
        ACCEPTANCE_CONTRACTS_DIRECTORY,
        stale_directory_documents,
    )

    stale_contracts = loader.load_acceptance_contracts()
    assert stale_contracts[0].title == "Stale Acceptance Contract Override"

    fresh_directory_documents = original_contract_documents[1:]
    loader.set_validated_directory_override(
        ACCEPTANCE_CONTRACTS_DIRECTORY,
        fresh_directory_documents,
    )

    refreshed_contracts = loader.load_acceptance_contracts()
    refreshed_contract_ids = {contract.contract_id for contract in refreshed_contracts}
    refreshed_removed_document = loader.load_validated_document(removed_path)

    assert refreshed_removed_document["title"] == removed_document["title"]
    assert stale_contracts != refreshed_contracts
    assert refreshed_contract_ids == {document["id"] for _, document in fresh_directory_documents}


def test_control_plane_loader_invalidates_merged_validator_registry_after_core_override() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    original_registry = loader.load_validator_registry()
    updated_document = deepcopy(loader.load_validated_document(VALIDATOR_REGISTRY_PATH))

    for validator in updated_document["validators"]:
        if validator["id"] == "validator.control_plane.acceptance_contract":
            validator["title"] = "Updated Acceptance Contract Validator"
            break
    else:
        raise AssertionError("Expected shared validator entry to exist in core registry.")

    loader.set_validated_document_override(VALIDATOR_REGISTRY_PATH, updated_document)

    refreshed_registry = loader.load_validator_registry()

    assert refreshed_registry is not original_registry
    assert (
        refreshed_registry.get("validator.control_plane.acceptance_contract").title
        == "Updated Acceptance Contract Validator"
    )


def test_control_plane_loader_document_override_invalidates_cached_parent_directory_state() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    original_contracts = loader.load_acceptance_contracts()
    original_contract = original_contracts[0]
    updated_document = deepcopy(loader.load_validated_document(original_contract.doc_path))
    updated_document["title"] = "Updated Acceptance Contract Title"

    loader.set_validated_document_override(original_contract.doc_path, updated_document)

    refreshed_contracts = loader.load_acceptance_contracts()
    refreshed_contract = next(
        contract
        for contract in refreshed_contracts
        if contract.doc_path == original_contract.doc_path
    )

    assert refreshed_contracts is not original_contracts
    assert refreshed_contract.title == "Updated Acceptance Contract Title"


def test_control_plane_loader_derive_does_not_reuse_stale_typed_caches(
    tmp_path: Path,
) -> None:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)

    loader = ControlPlaneLoader(repo_root)
    original_registry = loader.load_validator_registry()
    registry_path = repo_root / VALIDATOR_REGISTRY_PATH
    updated_document = json.loads(registry_path.read_text(encoding="utf-8"))
    updated_document["title"] = "Updated Validator Registry Title"
    registry_path.write_text(f"{json.dumps(updated_document, indent=2)}\n", encoding="utf-8")

    derived = loader.derive()
    refreshed_registry = derived.load_validator_registry()

    assert original_registry.title != "Updated Validator Registry Title"
    assert refreshed_registry.title == "Updated Validator Registry Title"


def test_control_plane_loader_allows_identical_copied_shared_validator_entries(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "oversight")
    pack_validator_registry_path = (
        repo_root
        / surfaces["pack_settings_path"].rsplit("/", maxsplit=2)[0]
        / "registries"
        / "validator_registry.json"
    )
    pack_validator_registry = json.loads(pack_validator_registry_path.read_text(encoding="utf-8"))
    core_validator_registry = json.loads(
        (repo_root / VALIDATOR_REGISTRY_PATH).read_text(encoding="utf-8")
    )
    copied_shared_validator = next(
        validator
        for validator in core_validator_registry["validators"]
        if validator["id"] == "validator.control_plane.acceptance_contract"
    )
    pack_validator_registry["validators"].insert(0, copied_shared_validator)
    pack_validator_registry_path.write_text(
        f"{json.dumps(pack_validator_registry, indent=2)}\n",
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    merged_registry = loader.load_validator_registry()

    acceptance_contract_entries = [
        validator
        for validator in merged_registry.validators
        if validator.validator_id == "validator.control_plane.acceptance_contract"
    ]

    assert len(acceptance_contract_entries) == 1
