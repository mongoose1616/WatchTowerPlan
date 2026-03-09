"""Minimal GitHub API client for issue and project sync."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


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
        owner_field = self._owner_field(owner_type)
        query = f"""
        query($login: String!, $number: Int!) {{
          {owner_field}(login: $login) {{
            projectV2(number: $number) {{
              id
              fields(first: 50) {{
                nodes {{
                  ... on ProjectV2SingleSelectField {{
                    id
                    name
                    options {{
                      id
                      name
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        """
        response = self._graphql_json(
            query,
            {"login": owner, "number": number},
        )
        owner_payload = response.get(owner_field)
        if not isinstance(owner_payload, dict):
            raise GitHubApiError(f"GitHub project owner not found: {owner_type} {owner}")
        project = owner_payload.get("projectV2")
        if not isinstance(project, dict):
            raise GitHubApiError(f"GitHub project not found: {owner} #{number}")

        field_nodes = project.get("fields", {}).get("nodes", [])
        if not isinstance(field_nodes, list):
            raise GitHubApiError("GitHub project fields response is malformed.")

        for node in field_nodes:
            if not isinstance(node, dict):
                continue
            if node.get("name") != status_field_name:
                continue
            options = node.get("options", [])
            if not isinstance(options, list):
                raise GitHubApiError("GitHub project status field options are malformed.")
            option_map: dict[str, str] = {}
            for option in options:
                if not isinstance(option, dict):
                    continue
                option_id = option.get("id")
                option_name = option.get("name")
                if isinstance(option_id, str) and isinstance(option_name, str):
                    option_map[option_name] = option_id
            field_id = node.get("id")
            if not isinstance(field_id, str) or not field_id:
                raise GitHubApiError("GitHub project status field is missing its identifier.")
            return GitHubProjectContext(
                owner=owner,
                owner_type=owner_type,
                number=number,
                project_id=str(project["id"]),
                status_field_name=status_field_name,
                status_field_id=field_id,
                status_options=option_map,
            )

        raise GitHubApiError(
            f"GitHub project #{number} for {owner} does not have a single-select "
            f"field named {status_field_name!r}."
        )

    def find_project_item_id(
        self,
        project: GitHubProjectContext,
        *,
        issue_node_id: str,
    ) -> str | None:
        owner_field = self._owner_field(project.owner_type)
        cursor: str | None = None
        while True:
            query = f"""
            query($login: String!, $number: Int!, $cursor: String) {{
              {owner_field}(login: $login) {{
                projectV2(number: $number) {{
                  items(first: 100, after: $cursor) {{
                    nodes {{
                      id
                      content {{
                        ... on Issue {{
                          id
                        }}
                      }}
                    }}
                    pageInfo {{
                      hasNextPage
                      endCursor
                    }}
                  }}
                }}
              }}
            }}
            """
            response = self._graphql_json(
                query,
                {
                    "login": project.owner,
                    "number": project.number,
                    "cursor": cursor,
                },
            )
            owner_payload = response.get(owner_field)
            if not isinstance(owner_payload, dict):
                raise GitHubApiError("GitHub project owner payload is malformed.")
            project_payload = owner_payload.get("projectV2")
            if not isinstance(project_payload, dict):
                raise GitHubApiError("GitHub project payload is malformed.")
            items_payload = project_payload.get("items", {})
            nodes = items_payload.get("nodes", [])
            if not isinstance(nodes, list):
                raise GitHubApiError("GitHub project items payload is malformed.")
            for node in nodes:
                if not isinstance(node, dict):
                    continue
                content = node.get("content")
                if not isinstance(content, dict):
                    continue
                if content.get("id") == issue_node_id:
                    item_id = node.get("id")
                    if isinstance(item_id, str) and item_id:
                        return item_id
            page_info = items_payload.get("pageInfo", {})
            if not isinstance(page_info, dict) or not page_info.get("hasNextPage"):
                return None
            end_cursor = page_info.get("endCursor")
            cursor = end_cursor if isinstance(end_cursor, str) and end_cursor else None
            if cursor is None:
                return None

    def add_project_item(
        self,
        project: GitHubProjectContext,
        *,
        issue_node_id: str,
    ) -> str:
        mutation = """
        mutation($projectId: ID!, $contentId: ID!) {
          addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
            item {
              id
            }
          }
        }
        """
        response = self._graphql_json(
            mutation,
            {"projectId": project.project_id, "contentId": issue_node_id},
        )
        payload = response.get("addProjectV2ItemById")
        if not isinstance(payload, dict):
            raise GitHubApiError("GitHub project add-item response is malformed.")
        item = payload.get("item")
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise GitHubApiError("GitHub project add-item response is missing the item ID.")
        return str(item["id"])

    def update_project_status(
        self,
        project: GitHubProjectContext,
        *,
        item_id: str,
        status_name: str,
    ) -> None:
        option_id = project.status_options.get(status_name)
        if option_id is None:
            available = ", ".join(sorted(project.status_options))
            raise GitHubApiError(
                f"GitHub project status option {status_name!r} is not available on "
                f"{project.owner} project #{project.number}. Available options: {available}"
            )
        mutation = """
        mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
          updateProjectV2ItemFieldValue(
            input: {
              projectId: $projectId
              itemId: $itemId
              fieldId: $fieldId
              value: {singleSelectOptionId: $optionId}
            }
          ) {
            projectV2Item {
              id
            }
          }
        }
        """
        self._graphql_json(
            mutation,
            {
                "projectId": project.project_id,
                "itemId": item_id,
                "fieldId": project.status_field_id,
                "optionId": option_id,
            },
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
        try:
            number = int(document["number"])
            node_id = str(document["node_id"])
            html_url = str(document["html_url"])
            state = str(document["state"])
        except (KeyError, TypeError, ValueError) as exc:
            raise GitHubApiError("GitHub issue response is missing required fields.") from exc
        return GitHubIssueRef(
            repository=repository,
            number=number,
            node_id=node_id,
            html_url=html_url,
            state=state,
        )

    @staticmethod
    def _owner_field(owner_type: str) -> str:
        if owner_type == "organization":
            return "organization"
        if owner_type == "user":
            return "user"
        raise GitHubApiError(f"Unsupported GitHub project owner type: {owner_type}")
