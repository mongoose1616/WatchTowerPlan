"""Shared GitHub integration models and error types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GitHubIssueRef:
    """Resolved GitHub issue identity returned by sync operations."""

    repository: str
    number: int
    node_id: str
    html_url: str
    state: str


@dataclass(frozen=True, slots=True)
class GitHubProjectContext:
    """Resolved GitHub project identity and its status-field options."""

    owner: str
    owner_type: str
    number: int
    project_id: str
    status_field_name: str
    status_field_id: str
    status_options: dict[str, str]


@dataclass(frozen=True, slots=True)
class GitHubLabelSpec:
    """Managed GitHub label definition used by repo-local sync flows."""

    name: str
    color: str
    description: str | None = None


class GitHubApiError(RuntimeError):
    """Raised when a GitHub REST or GraphQL request fails."""
