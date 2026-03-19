from __future__ import annotations

import json
from pathlib import Path

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.rebuild import RebuildHarness, RebuildOutput, RebuildTargetSpec

REPO_ROOT = Path(__file__).resolve().parents[4]
PLAN_INITIATIVE_INDEX_PATH = "plan/.wt/indexes/initiative_index.json"


def test_rebuild_harness_writes_json_and_markdown_outputs_to_output_dir(
    tmp_path: Path,
) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    document = loader.load_validated_document(PLAN_INITIATIVE_INDEX_PATH)

    result = RebuildHarness(loader).run_specs(
        (
            RebuildTargetSpec(
                target="fixture-rebuild",
                build_outputs=lambda _loader: (
                    RebuildOutput(
                        relative_output_path=PLAN_INITIATIVE_INDEX_PATH,
                        artifact_kind="index",
                        output_format="json",
                        content=document,
                        validated=True,
                    ),
                    RebuildOutput(
                        relative_output_path="plan/rebuild_fixture.md",
                        artifact_kind="rendered_view",
                        output_format="markdown",
                        content="# Fixture Rebuild",
                    ),
                ),
            ),
        ),
        output_dir=tmp_path,
    )

    assert result.wrote is True
    assert result.output_dir == str(tmp_path.resolve())
    assert len(result.records) == 2

    rebuilt_document = json.loads((tmp_path / PLAN_INITIATIVE_INDEX_PATH).read_text(encoding="utf-8"))
    assert rebuilt_document == document
    assert (tmp_path / "plan/rebuild_fixture.md").read_text(encoding="utf-8") == (
        "# Fixture Rebuild\n"
    )


def test_rebuild_harness_reuses_json_overrides_between_specs(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    document = dict(loader.load_validated_document(PLAN_INITIATIVE_INDEX_PATH))
    document["title"] = "Runtime Override Initiative Index"

    result = RebuildHarness(loader).run_specs(
        (
            RebuildTargetSpec(
                target="override-source",
                build_outputs=lambda _loader: (
                    RebuildOutput(
                        relative_output_path=PLAN_INITIATIVE_INDEX_PATH,
                        artifact_kind="index",
                        output_format="json",
                        content=document,
                        validated=True,
                    ),
                ),
            ),
            RebuildTargetSpec(
                target="override-consumer",
                build_outputs=lambda runtime_loader: (
                    RebuildOutput(
                        relative_output_path="plan/rebuild_override.md",
                        artifact_kind="rendered_view",
                        output_format="markdown",
                        content=(
                            "# "
                            + str(
                                runtime_loader.load_validated_document(
                                    PLAN_INITIATIVE_INDEX_PATH
                                )["title"]
                            )
                        ),
                    ),
                ),
            ),
        ),
        output_dir=tmp_path,
    )

    assert len(result.records) == 2
    assert (tmp_path / "plan/rebuild_override.md").read_text(encoding="utf-8") == (
        "# Runtime Override Initiative Index\n"
    )


def test_rebuild_harness_fails_closed_on_duplicate_output_paths(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    with pytest.raises(ValueError, match="same output path more than once"):
        RebuildHarness(loader).run_specs(
            (
                RebuildTargetSpec(
                    target="first",
                    build_outputs=lambda _loader: (
                        RebuildOutput(
                            relative_output_path="plan/duplicate.md",
                            artifact_kind="rendered_view",
                            output_format="markdown",
                            content="# First",
                        ),
                    ),
                ),
                RebuildTargetSpec(
                    target="second",
                    build_outputs=lambda _loader: (
                        RebuildOutput(
                            relative_output_path="plan/duplicate.md",
                            artifact_kind="rendered_view",
                            output_format="markdown",
                            content="# Second",
                        ),
                    ),
                ),
            ),
            output_dir=tmp_path,
        )
