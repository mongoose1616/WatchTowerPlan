"""Minimal GitHub API client for issue and project sync."""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from watchtower_core.integrations.github.client_project_support import (
    add_project_item,
    find_project_item_id,
    issue_from_document,
    load_project_context,
    owner_field,
    update_project_status,
)
from watchtower_core.integrations.github.models import (
    GitHubApiError,
    GitHubIssueRef,
    GitHubLabelSpec,
    GitHubProjectContext,
)


class GitHubClient:
    """Thin GitHub client that covers the issue and Projects surfaces this repo uses."""

    def __init__(
        self,
        token: str,
        *,
        api_base_url: str = "https://api.github.com",
        graphql_url: str = "https://api.github.com/graphql",
    ) -> None:
        self._token = token
        self._api_base_url = api_base_url.rstrip("/")
        self._graphql_url = graphql_url

    @classmethod
    def from_env(cls, token_env: str = "GITHUB_TOKEN") -> GitHubClient:
        token = os.environ.get(token_env)
        if token is None or not token.strip():
            raise GitHubApiError(
                f"Missing GitHub token in environment variable {token_env}."
            )
        return cls(token.strip())

    def create_issue(
        self,
        repository: str,
        *,
        title: str,
        body: str,
        labels: tuple[str, ...] = (),
        state: str = "open",
        state_reason: str | None = None,
    ) -> GitHubIssueRef:
        response = self._rest_json(
            "POST",
            f"/repos/{repository}/issues",
            payload={
                "title": title,
                "body": body,
                **({"labels": list(labels)} if labels else {}),
            },
        )
        issue = self._issue_from_document(repository, response)
        if state == "closed":
            return self.update_issue(
                repository,
                issue.number,
                title=title,
                body=body,
                state=state,
                state_reason=state_reason,
            )
        return issue

    def update_issue(
        self,
        repository: str,
        issue_number: int,
        *,
        title: str,
        body: str,
        labels: tuple[str, ...] = (),
        state: str,
        state_reason: str | None = None,
    ) -> GitHubIssueRef:
        payload: dict[str, object] = {
            "title": title,
            "body": body,
            "state": state,
        }
        if labels:
            payload["labels"] = list(labels)
        if state == "closed" and state_reason is not None:
            payload["state_reason"] = state_reason
        response = self._rest_json(
            "PATCH",
            f"/repos/{repository}/issues/{issue_number}",
            payload=payload,
        )
        return self._issue_from_document(repository, response)

    def ensure_labels(
        self,
        repository: str,
        labels: tuple[GitHubLabelSpec, ...],
    ) -> None:
        """Ensure the managed label set exists on the target repository."""
        for label in labels:
            existing = self._rest_json_or_none(
                "GET",
                f"/repos/{repository}/labels/{quote(label.name, safe='')}",
            )
            if existing is not None:
                continue
            payload: dict[str, object] = {
                "name": label.name,
                "color": label.color,
            }
            if label.description is not None:
                payload["description"] = label.description
            self._rest_json(
                "POST",
                f"/repos/{repository}/labels",
                payload=payload,
            )

    def load_project_context(
        self,
        *,
        owner: str,
        owner_type: str,
        number: int,
        status_field_name: str = "Status",
    ) -> GitHubProjectContext:
        return load_project_context(
            owner=owner,
            owner_type=owner_type,
            number=number,
            status_field_name=status_field_name,
            graphql_json=self._graphql_json,
        )

    def find_project_item_id(
        self,
        project: GitHubProjectContext,
        *,
        issue_node_id: str,
    ) -> str | None:
        return find_project_item_id(
            project,
            issue_node_id=issue_node_id,
            graphql_json=self._graphql_json,
        )

    def add_project_item(
        self,
        project: GitHubProjectContext,
        *,
        issue_node_id: str,
    ) -> str:
        return add_project_item(
            project,
            issue_node_id=issue_node_id,
            graphql_json=self._graphql_json,
        )

    def update_project_status(
        self,
        project: GitHubProjectContext,
        *,
        item_id: str,
        status_name: str,
    ) -> None:
        update_project_status(
            project,
            item_id=item_id,
            status_name=status_name,
            graphql_json=self._graphql_json,
        )

    def _rest_json(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, object] | None = None,
    ) -> dict[str, Any]:
        url = f"{self._api_base_url}{path}"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self._token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        data = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = Request(url, data=data, headers=headers, method=method)
        return self._load_json_response(request)

    def _graphql_json(
        self,
        query: str,
        variables: dict[str, object],
    ) -> dict[str, Any]:
        payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
        request = Request(
            self._graphql_url,
            data=payload,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            method="POST",
        )
        response = self._load_json_response(request)
        errors = response.get("errors")
        if isinstance(errors, list) and errors:
            messages = []
            for error in errors:
                if isinstance(error, dict):
                    message = error.get("message")
                    if isinstance(message, str):
                        messages.append(message)
            joined = "; ".join(messages) if messages else "Unknown GraphQL error"
            raise GitHubApiError(joined)
        data = response.get("data")
        if not isinstance(data, dict):
            raise GitHubApiError("GitHub GraphQL response is missing its data payload.")
        return data

    def _rest_json_or_none(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, object] | None = None,
    ) -> dict[str, Any] | None:
        try:
            return self._rest_json(method, path, payload=payload)
        except GitHubApiError as exc:
            if "with 404:" in str(exc):
                return None
            raise

    def _load_json_response(self, request: Request) -> dict[str, Any]:
        try:
            with urlopen(request) as response:
                payload = response.read().decode("utf-8")
        except HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise GitHubApiError(
                f"GitHub API request failed with {exc.code}: {details}"
            ) from exc
        except URLError as exc:
            raise GitHubApiError(f"GitHub API request failed: {exc.reason}") from exc

        loaded = json.loads(payload)
        if not isinstance(loaded, dict):
            raise GitHubApiError("GitHub API response was not a JSON object.")
        return loaded

    @staticmethod
    def _issue_from_document(repository: str, document: dict[str, Any]) -> GitHubIssueRef:
        return issue_from_document(repository, document)

    @staticmethod
    def _owner_field(owner_type: str) -> str:
        return owner_field(owner_type)
