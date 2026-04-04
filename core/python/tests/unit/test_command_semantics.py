from __future__ import annotations

import pytest

from tests.pack_fixture_support import materialize_validation_repo_subset
from watchtower_core.documentation.command_semantics import validate_command_document


def test_validate_command_document_rejects_duplicate_related_command_surfaces(
    tmp_path,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    relative_path = "core/docs/commands/core_python/watchtower_core_query_acceptance.md"
    resolved_path = repo_root / relative_path

    markdown = resolved_path.read_text(encoding="utf-8")
    markdown = markdown.replace(
        "| `watchtower-core validate acceptance` | Performs semantic reconciliation across "
        "the same trace surfaces. |\n",
        "| `watchtower-core query evidence` | Duplicate row used to prove repeated command "
        "surfaces fail closed. |\n",
        1,
    )
    resolved_path.write_text(markdown, encoding="utf-8")

    with pytest.raises(ValueError, match="repeats the same command surface more than once"):
        validate_command_document(
            relative_path=relative_path,
            resolved_path=resolved_path,
            repo_root=repo_root,
        )


def test_validate_command_document_allows_distinct_pack_namespace_sync_subcommands(
    tmp_path,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    relative_path = "core/docs/commands/core_python/watchtower_core_sync.md"
    resolved_path = repo_root / relative_path

    validate_command_document(
        relative_path=relative_path,
        resolved_path=resolved_path,
        repo_root=repo_root,
    )
