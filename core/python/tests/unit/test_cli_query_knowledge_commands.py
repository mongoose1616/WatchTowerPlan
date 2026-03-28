from __future__ import annotations

from tests.cli_command_helpers import run_json_command
from watchtower_host.cli.main import main


def test_query_authority_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "authority",
            "--artifact-kind",
            "template_catalog",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query authority"
    assert payload["status"] == "ok"
    assert payload["result_count"] >= 1
    assert all(entry["artifact_kind"] == "template_catalog" for entry in payload["results"])
    assert {
        "question_id",
        "domain",
        "question",
        "status",
        "artifact_kind",
        "canonical_path",
        "preferred_command",
        "status_fields",
        "fallback_paths",
        "aliases",
        "notes",
    }.issubset(payload["results"][0])


def test_query_templates_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "templates",
            "--allowed-root",
            "core/docs/commands",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query templates"
    assert payload["status"] == "ok"
    assert payload["result_count"] >= 1
    assert all("core/docs/commands" in entry["allowed_roots"] for entry in payload["results"])
    assert {
        "template_id",
        "surface_id",
        "entry_status",
        "authorship_mode",
        "template_path",
        "required_section_ids",
        "section_order",
        "llm_guidance_mode",
        "allowed_roots",
    }.issubset(payload["results"][0])


def test_query_help_lists_authority_and_templates(capsys) -> None:
    result = main(["query"])

    help_text = capsys.readouterr().out
    assert result == 0
    assert "authority" in help_text
    assert "templates" in help_text


def test_query_commands_discovers_authority_and_template_leaves(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "commands",
            "--query",
            "watchtower-core query authority",
            "--limit",
            "10",
        ],
    )

    assert result == 0
    assert any(
        entry["command"] == "watchtower-core query authority" for entry in payload["results"]
    )

    result, payload = run_json_command(
        capsys,
        [
            "query",
            "commands",
            "--query",
            "watchtower-core query templates",
            "--limit",
            "10",
        ],
    )

    assert result == 0
    assert any(
        entry["command"] == "watchtower-core query templates" for entry in payload["results"]
    )
