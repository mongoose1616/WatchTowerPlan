"""GitHub integration helpers for local-first sync surfaces."""

from watchtower_core.integrations.github.client import (
    GitHubApiError,
    GitHubClient,
    GitHubIssueRef,
    GitHubLabelSpec,
    GitHubProjectContext,
)

__all__ = [
    "GitHubApiError",
    "GitHubClient",
    "GitHubIssueRef",
    "GitHubLabelSpec",
    "GitHubProjectContext",
]
