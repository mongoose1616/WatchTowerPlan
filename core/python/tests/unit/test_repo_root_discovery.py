from __future__ import annotations

from pathlib import Path

import pytest

from watchtower_core.control_plane.errors import RepoRootNotFoundError
from watchtower_core.control_plane.paths import discover_repo_root

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_discover_repo_root_prefers_current_worktree(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    repo_root = tmp_path / "worktree"
    (repo_root / "core/control_plane").mkdir(parents=True)
    (repo_root / "core/python").mkdir(parents=True)

    monkeypatch.chdir(repo_root / "core/python")

    assert discover_repo_root() == repo_root


def test_discover_repo_root_falls_back_to_package_checkout(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    outside_directory = tmp_path / "outside"
    outside_directory.mkdir(parents=True)
    monkeypatch.chdir(outside_directory)

    with pytest.raises(RepoRootNotFoundError):
        discover_repo_root()


def test_discover_repo_root_can_explicitly_fall_back_to_package_checkout(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    outside_directory = tmp_path / "outside"
    outside_directory.mkdir(parents=True)
    monkeypatch.chdir(outside_directory)

    assert discover_repo_root(allow_package_checkout_fallback=True) == REPO_ROOT


def test_discover_repo_root_rejects_explicit_non_repo_start(tmp_path: Path) -> None:
    outside_directory = tmp_path / "outside"
    outside_directory.mkdir(parents=True)

    with pytest.raises(RepoRootNotFoundError):
        discover_repo_root(outside_directory)
