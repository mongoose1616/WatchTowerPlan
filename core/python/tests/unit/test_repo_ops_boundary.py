import importlib
import sys
from pathlib import Path

import pytest

import watchtower_core.query as public_query
import watchtower_core.sync as public_sync
import watchtower_core.validation as public_validation
from watchtower_core.repo_ops.query.commands import CommandQueryService
from watchtower_core.repo_ops.sync.command_index import CommandIndexSyncService
from watchtower_core.repo_ops.validation import (
    DocumentSemanticsValidationService,
    WATCHTOWER_PLAN_VALIDATION_SUITE_ID,
    resolve_watchtower_plan_suite_targets,
)
from watchtower_core.validation.all import ValidationAllService

PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "src" / "watchtower_core"


def test_public_query_root_fails_closed_with_repo_ops_guidance() -> None:
    with pytest.raises(AttributeError, match="watchtower_core.repo_ops.query"):
        _ = public_query.CommandQueryService


def test_public_sync_root_fails_closed_with_repo_ops_guidance() -> None:
    with pytest.raises(AttributeError, match="watchtower_core.repo_ops.sync"):
        _ = public_sync.CommandIndexSyncService


def test_public_validation_root_fails_closed_with_repo_ops_guidance() -> None:
    with pytest.raises(AttributeError, match="watchtower_core.validation.all"):
        _ = public_validation.ValidationAllService
    with pytest.raises(AttributeError, match="watchtower_core.repo_ops.validation"):
        _ = public_validation.DocumentSemanticsValidationService


def test_query_and_sync_package_roots_do_not_ship_repo_specific_leaf_modules() -> None:
    assert sorted(path.name for path in (PACKAGE_ROOT / "query").glob("*.py")) == ["__init__.py"]
    assert sorted(path.name for path in (PACKAGE_ROOT / "sync").glob("*.py")) == ["__init__.py"]


@pytest.mark.parametrize(
    "module_name",
    (
        "watchtower_core.query.commands",
        "watchtower_core.query.foundations",
        "watchtower_core.query.traceability",
        "watchtower_core.sync.all",
        "watchtower_core.sync.command_index",
        "watchtower_core.sync.traceability",
        "watchtower_core.validation.document_semantics",
        "watchtower_core.validation.registry",
        "watchtower_core.repo_ops.validation.all",
        "watchtower_core.repo_ops.validation.registry",
    ),
)
def test_retired_wrapper_modules_are_not_importable(module_name: str) -> None:
    sys.modules.pop(module_name, None)
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module(module_name)


def test_repo_ops_boundary_owners_remain_available() -> None:
    assert CommandQueryService.__module__ == "watchtower_core.repo_ops.query.commands"
    assert CommandIndexSyncService.__module__ == "watchtower_core.repo_ops.sync.command_index"
    assert ValidationAllService.__module__ == "watchtower_core.validation.all"
    assert (
        DocumentSemanticsValidationService.__module__
        == "watchtower_core.repo_ops.validation.document_semantics"
    )
    assert (
        resolve_watchtower_plan_suite_targets.__module__
        == "watchtower_core.repo_ops.validation.targets"
    )
    assert WATCHTOWER_PLAN_VALIDATION_SUITE_ID == "suite.watchtower_plan.validation_baseline"
