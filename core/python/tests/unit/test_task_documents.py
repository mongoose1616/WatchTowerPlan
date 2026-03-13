from __future__ import annotations

from pathlib import Path
from shutil import copytree

import pytest

from tests.integration.fixture_repo_support import materialize_governed_applies_to_targets
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops import task_documents as task_documents_module

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    copytree(REPO_ROOT / "docs" / "planning", repo_root / "docs" / "planning")
    (repo_root / "core" / "python").mkdir(parents=True)
    materialize_governed_applies_to_targets(repo_root)
    return repo_root


def test_iter_task_documents_skips_task_paths_that_disappear_before_load(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    baseline_documents = task_documents_module.iter_task_documents(loader)
    missing_relative_path = baseline_documents[0].relative_path
    original_loader = task_documents_module.load_task_document

    def _load_task_document(loader_arg: ControlPlaneLoader, relative_path: str):
        if relative_path == missing_relative_path:
            raise FileNotFoundError(relative_path)
        return original_loader(loader_arg, relative_path)

    monkeypatch.setattr(task_documents_module, "load_task_document", _load_task_document)

    documents = task_documents_module.iter_task_documents(loader)

    assert len(documents) == len(baseline_documents) - 1
    assert all(document.relative_path != missing_relative_path for document in documents)


def test_iter_task_documents_still_raises_for_non_missing_load_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    failing_relative_path = task_documents_module.iter_task_documents(loader)[0].relative_path
    original_loader = task_documents_module.load_task_document

    def _load_task_document(loader_arg: ControlPlaneLoader, relative_path: str):
        if relative_path == failing_relative_path:
            raise ValueError("simulated validation failure")
        return original_loader(loader_arg, relative_path)

    monkeypatch.setattr(task_documents_module, "load_task_document", _load_task_document)

    with pytest.raises(ValueError, match="simulated validation failure"):
        task_documents_module.iter_task_documents(loader)
