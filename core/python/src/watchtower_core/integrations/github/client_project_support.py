"""Project-query and response helpers for the GitHub client."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from watchtower_core.integrations.github.models import (
    GitHubApiError,
    GitHubIssueRef,
    GitHubProjectContext,
)

GraphQLInvoker = Callable[[str, dict[str, object]], dict[str, Any]]


def issue_from_document(repository: str, document: dict[str, Any]) -> GitHubIssueRef:
    """Build one issue reference from a GitHub REST payload."""

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


def owner_field(owner_type: str) -> str:
    """Resolve the GraphQL owner field for a supported project owner type."""

    if owner_type == "organization":
        return "organization"
    if owner_type == "user":
        return "user"
    raise GitHubApiError(f"Unsupported GitHub project owner type: {owner_type}")


def load_project_context(
    *,
    owner: str,
    owner_type: str,
    number: int,
    status_field_name: str,
    graphql_json: GraphQLInvoker,
) -> GitHubProjectContext:
    """Load one project context and its single-select status-field options."""

    resolved_owner_field = owner_field(owner_type)
    query = f"""
    query($login: String!, $number: Int!) {{
      {resolved_owner_field}(login: $login) {{
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
    response = graphql_json(query, {"login": owner, "number": number})
    owner_payload = response.get(resolved_owner_field)
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
    project: GitHubProjectContext,
    *,
    issue_node_id: str,
    graphql_json: GraphQLInvoker,
) -> str | None:
    """Find the existing project item linked to one issue node."""

    resolved_owner_field = owner_field(project.owner_type)
    cursor: str | None = None
    while True:
        query = f"""
        query($login: String!, $number: Int!, $cursor: String) {{
          {resolved_owner_field}(login: $login) {{
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
        response = graphql_json(
            query,
            {
                "login": project.owner,
                "number": project.number,
                "cursor": cursor,
            },
        )
        owner_payload = response.get(resolved_owner_field)
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
    project: GitHubProjectContext,
    *,
    issue_node_id: str,
    graphql_json: GraphQLInvoker,
) -> str:
    """Create one new project item for the issue node."""

    mutation = """
    mutation($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
        item {
          id
        }
      }
    }
    """
    response = graphql_json(
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
    project: GitHubProjectContext,
    *,
    item_id: str,
    status_name: str,
    graphql_json: GraphQLInvoker,
) -> None:
    """Update the project's single-select status field for one item."""

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
    graphql_json(
        mutation,
        {
            "projectId": project.project_id,
            "itemId": item_id,
            "fieldId": project.status_field_id,
            "optionId": option_id,
        },
    )
