"""Public rebuild namespace for export-safe generic derived-surface rebuilds."""

from __future__ import annotations

from watchtower_core.rebuild.harness import (
    RebuildBuilder,
    RebuildHarness,
    RebuildOutput,
    RebuildOutputFormat,
    RebuildRecord,
    RebuildResult,
    RebuildTargetSpec,
)
from watchtower_core.rebuild.rendered_views import (
    MarkdownReconciliationCode,
    MarkdownReconciliationHelper,
    MarkdownReconciliationIssue,
    RenderedViewBuilder,
    RenderedViewResult,
    RenderedViewSpec,
)
from watchtower_core.utils.module_exports import fail_closed_package_getattr

__all__ = [
    "MarkdownReconciliationCode",
    "MarkdownReconciliationHelper",
    "MarkdownReconciliationIssue",
    "RebuildBuilder",
    "RebuildHarness",
    "RebuildOutput",
    "RebuildOutputFormat",
    "RebuildRecord",
    "RebuildResult",
    "RebuildTargetSpec",
    "RenderedViewBuilder",
    "RenderedViewResult",
    "RenderedViewSpec",
]
__getattr__ = fail_closed_package_getattr(
    "watchtower_core.rebuild exports only generic rebuild harness surfaces. "
    "Repo-specific rebuild orchestration still lives under watchtower_plan."
)
