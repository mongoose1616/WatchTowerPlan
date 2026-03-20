"""Helpers for repairing moved task paths in governed companion artifacts."""

from __future__ import annotations

from copy import deepcopy

from watchtower_core.control_plane.loader import (
    ACCEPTANCE_CONTRACTS_DIRECTORY,
    VALIDATION_EVIDENCE_DIRECTORY,
    ControlPlaneLoader,
)


def repair_governed_task_path_references(
    loader: ControlPlaneLoader,
    *,
    previous_doc_path: str,
    current_doc_path: str,
) -> None:
    """Rewrite moved task paths in governed companion artifacts."""

    _rewrite_acceptance_contract_paths(
        loader,
        previous_doc_path=previous_doc_path,
        current_doc_path=current_doc_path,
    )
    _rewrite_validation_evidence_paths(
        loader,
        previous_doc_path=previous_doc_path,
        current_doc_path=current_doc_path,
    )


def _rewrite_acceptance_contract_paths(
    loader: ControlPlaneLoader,
    *,
    previous_doc_path: str,
    current_doc_path: str,
) -> None:
    updated_documents: list[tuple[str, dict[str, object]]] = []
    changed_any = False
    for relative_path, document in loader.iter_validated_documents_with_paths_under(
        ACCEPTANCE_CONTRACTS_DIRECTORY
    ):
        rewritten = deepcopy(document)
        changed = False
        entries = rewritten.get("entries")
        if isinstance(entries, list):
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                changed |= _replace_list_path(
                    entry,
                    "validation_targets",
                    previous_doc_path,
                    current_doc_path,
                )
                changed |= _replace_list_path(
                    entry,
                    "related_paths",
                    previous_doc_path,
                    current_doc_path,
                )
        if changed:
            loader.schema_store.validate_instance(rewritten)
            loader.artifact_store.write_json_object(relative_path, rewritten)
            changed_any = True
            updated_documents.append((relative_path, rewritten))
        else:
            updated_documents.append((relative_path, document))
    if changed_any:
        loader.set_validated_directory_override(
            ACCEPTANCE_CONTRACTS_DIRECTORY,
            tuple(updated_documents),
        )


def _rewrite_validation_evidence_paths(
    loader: ControlPlaneLoader,
    *,
    previous_doc_path: str,
    current_doc_path: str,
) -> None:
    updated_documents: list[tuple[str, dict[str, object]]] = []
    changed_any = False
    for relative_path, document in loader.iter_validated_documents_with_paths_under(
        VALIDATION_EVIDENCE_DIRECTORY
    ):
        rewritten = deepcopy(document)
        changed = _replace_list_path(
            rewritten,
            "related_paths",
            previous_doc_path,
            current_doc_path,
        )
        checks = rewritten.get("checks")
        if isinstance(checks, list):
            for check in checks:
                if not isinstance(check, dict):
                    continue
                changed |= _replace_list_path(
                    check,
                    "subject_paths",
                    previous_doc_path,
                    current_doc_path,
                )
        if changed:
            loader.schema_store.validate_instance(rewritten)
            loader.artifact_store.write_json_object(relative_path, rewritten)
            changed_any = True
            updated_documents.append((relative_path, rewritten))
        else:
            updated_documents.append((relative_path, document))
    if changed_any:
        loader.set_validated_directory_override(
            VALIDATION_EVIDENCE_DIRECTORY,
            tuple(updated_documents),
        )


def _replace_list_path(
    document: dict[str, object],
    key: str,
    previous_doc_path: str,
    current_doc_path: str,
) -> bool:
    values = document.get(key)
    if not isinstance(values, list):
        return False

    changed = False
    rewritten: list[object] = []
    for value in values:
        if not isinstance(value, str):
            rewritten.append(value)
            continue
        replacement = current_doc_path if value == previous_doc_path else value
        if replacement != value:
            changed = True
        rewritten.append(replacement)

    if changed:
        document[key] = rewritten
    return changed
