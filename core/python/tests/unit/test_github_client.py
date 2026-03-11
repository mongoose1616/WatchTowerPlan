from __future__ import annotations

import io
import json
from types import SimpleNamespace
from urllib.error import HTTPError, URLError

import pytest

from watchtower_core.integrations.github.client import (
    GitHubApiError,
    GitHubClient,
    GitHubIssueRef,
    GitHubLabelSpec,
)


class _FakeResponse:
    def __init__(self, payload: str) -> None:
        self._payload = payload

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def read(self) -> bytes:
        return self._payload.encode("utf-8")


def test_github_client_from_env_requires_token(monkeypatch) -> None:
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    with pytest.raises(
        GitHubApiError,
        match="Missing GitHub token in environment variable GITHUB_TOKEN.",
    ):
        GitHubClient.from_env()


def test_create_issue_can_close_issue_after_creation(monkeypatch) -> None:
    client = GitHubClient("token")
    created_issue = GitHubIssueRef(
        repository="owner/repo",
        number=7,
        node_id="ISSUE_NODE",
        html_url="https://example/issues/7",
        state="open",
    )
    update_calls: list[tuple[object, ...]] = []

    def fake_rest_json(method: str, path: str, *, payload: dict[str, object] | None = None):
        assert method == "POST"
        assert path == "/repos/owner/repo/issues"
        assert payload == {"title": "Example", "body": "Body"}
        return {
            "number": 7,
            "node_id": "ISSUE_NODE",
            "html_url": "https://example/issues/7",
            "state": "open",
        }

    def fake_update_issue(
        repository: str,
        issue_number: int,
        *,
        title: str,
        body: str,
        labels: tuple[str, ...] = (),
        state: str,
        state_reason: str | None,
    ) -> GitHubIssueRef:
        update_calls.append((repository, issue_number, title, body, labels, state, state_reason))
        return GitHubIssueRef(
            repository=repository,
            number=issue_number,
            node_id=created_issue.node_id,
            html_url=created_issue.html_url,
            state="closed",
        )

    monkeypatch.setattr(client, "_rest_json", fake_rest_json)
    monkeypatch.setattr(client, "update_issue", fake_update_issue)

    result = client.create_issue(
        "owner/repo",
        title="Example",
        body="Body",
        state="closed",
        state_reason="completed",
    )

    assert result.state == "closed"
    assert update_calls == [
        ("owner/repo", 7, "Example", "Body", (), "closed", "completed")
    ]


def test_ensure_labels_creates_only_missing_labels(monkeypatch) -> None:
    client = GitHubClient("token")
    created_payloads: list[dict[str, object]] = []

    def fake_rest_json_or_none(
        method: str,
        path: str,
        *,
        payload: dict[str, object] | None = None,
    ) -> dict[str, object] | None:
        assert method == "GET"
        if path.endswith("/labels/existing"):
            return {"name": "existing"}
        return None

    def fake_rest_json(
        method: str,
        path: str,
        *,
        payload: dict[str, object] | None = None,
    ) -> dict[str, object]:
        assert method == "POST"
        assert path == "/repos/owner/repo/labels"
        assert payload is not None
        created_payloads.append(payload)
        return payload

    monkeypatch.setattr(client, "_rest_json_or_none", fake_rest_json_or_none)
    monkeypatch.setattr(client, "_rest_json", fake_rest_json)

    client.ensure_labels(
        "owner/repo",
        (
            GitHubLabelSpec(name="existing", color="ffffff"),
            GitHubLabelSpec(name="missing", color="0E8A16", description="Managed"),
        ),
    )

    assert created_payloads == [
        {"name": "missing", "color": "0E8A16", "description": "Managed"}
    ]


def test_load_project_context_returns_status_field_mapping(monkeypatch) -> None:
    client = GitHubClient("token")

    monkeypatch.setattr(
        client,
        "_graphql_json",
        lambda query, variables: {
            "organization": {
                "projectV2": {
                    "id": "PROJECT_ID",
                    "fields": {
                        "nodes": [
                            {
                                "id": "FIELD_ID",
                                "name": "Status",
                                "options": [
                                    {"id": "OPT_DONE", "name": "Done"},
                                    {"id": "OPT_READY", "name": "Ready"},
                                ],
                            }
                        ]
                    },
                }
            }
        },
    )

    result = client.load_project_context(owner="owner", owner_type="organization", number=12)

    assert result.project_id == "PROJECT_ID"
    assert result.status_field_id == "FIELD_ID"
    assert result.status_options == {"Done": "OPT_DONE", "Ready": "OPT_READY"}


def test_load_project_context_rejects_missing_status_field(monkeypatch) -> None:
    client = GitHubClient("token")

    monkeypatch.setattr(
        client,
        "_graphql_json",
        lambda query, variables: {
            "user": {
                "projectV2": {
                    "id": "PROJECT_ID",
                    "fields": {"nodes": [{"id": "FIELD", "name": "Priority", "options": []}]},
                }
            }
        },
    )

    with pytest.raises(
        GitHubApiError,
        match="does not have a single-select field named 'Status'",
    ):
        client.load_project_context(owner="owner", owner_type="user", number=7)


def test_find_project_item_id_paginates_until_match(monkeypatch) -> None:
    client = GitHubClient("token")
    project = SimpleNamespace(owner="owner", owner_type="organization", number=9)
    responses = iter(
        (
            {
                "organization": {
                    "projectV2": {
                        "items": {
                            "nodes": [],
                            "pageInfo": {"hasNextPage": True, "endCursor": "CURSOR_1"},
                        }
                    }
                }
            },
            {
                "organization": {
                    "projectV2": {
                        "items": {
                            "nodes": [
                                {"id": "ITEM_ID", "content": {"id": "ISSUE_NODE"}},
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        }
                    }
                }
            },
        )
    )

    monkeypatch.setattr(client, "_graphql_json", lambda query, variables: next(responses))

    result = client.find_project_item_id(project, issue_node_id="ISSUE_NODE")

    assert result == "ITEM_ID"


def test_update_project_status_rejects_unknown_status_option() -> None:
    client = GitHubClient("token")
    project = SimpleNamespace(
        owner="owner",
        number=3,
        project_id="PROJECT_ID",
        status_field_id="FIELD_ID",
        status_options={"Done": "OPT_DONE"},
    )

    with pytest.raises(
        GitHubApiError,
        match="Available options: Done",
    ):
        client.update_project_status(project, item_id="ITEM_ID", status_name="Blocked")


def test_graphql_json_raises_for_graphql_errors(monkeypatch) -> None:
    client = GitHubClient("token")
    monkeypatch.setattr(
        client,
        "_load_json_response",
        lambda request: {"errors": [{"message": "permission denied"}]},
    )

    with pytest.raises(GitHubApiError, match="permission denied"):
        client._graphql_json("query {}", {})


def test_load_json_response_wraps_http_and_network_errors(monkeypatch) -> None:
    client = GitHubClient("token")
    request = SimpleNamespace()

    def raise_http(request: object) -> _FakeResponse:
        raise HTTPError(
            url="https://api.github.com/repos/owner/repo/issues",
            code=500,
            msg="boom",
            hdrs=None,
            fp=io.BytesIO(b"server exploded"),
        )

    monkeypatch.setattr("watchtower_core.integrations.github.client.urlopen", raise_http)
    with pytest.raises(GitHubApiError, match="GitHub API request failed with 500: server exploded"):
        client._load_json_response(request)

    monkeypatch.setattr(
        "watchtower_core.integrations.github.client.urlopen",
        lambda request: (_ for _ in ()).throw(URLError("offline")),
    )
    with pytest.raises(GitHubApiError, match="GitHub API request failed: offline"):
        client._load_json_response(request)


def test_load_json_response_rejects_non_object_payload(monkeypatch) -> None:
    client = GitHubClient("token")
    monkeypatch.setattr(
        "watchtower_core.integrations.github.client.urlopen",
        lambda request: _FakeResponse(json.dumps([1, 2, 3])),
    )

    with pytest.raises(GitHubApiError, match="GitHub API response was not a JSON object."):
        client._load_json_response(SimpleNamespace())
