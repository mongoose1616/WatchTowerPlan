from __future__ import annotations

import argparse
import json

from watchtower_core.cli.handler_common import _emit_collection_query_results


def _args(*, format: str = "human") -> argparse.Namespace:
    return argparse.Namespace(format=format)


def test_emit_collection_query_results_supports_json_without_human_render(capsys) -> None:
    result = _emit_collection_query_results(
        _args(format="json"),
        command_name="watchtower-core query example",
        entries=("entry.example",),
        noun="example",
        empty_message="No example entries matched the requested filters.",
        payload_results_factory=lambda: [{"example_id": "entry.example"}],
        render_entry=lambda entry: (_ for _ in ()).throw(
            AssertionError("human rendering should not run for json output")
        ),
        extra_payload={"default_scope": "active"},
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload == {
        "command": "watchtower-core query example",
        "default_scope": "active",
        "result_count": 1,
        "results": [{"example_id": "entry.example"}],
        "status": "ok",
    }


def test_emit_collection_query_results_prints_human_summary(capsys) -> None:
    rendered: list[str] = []

    result = _emit_collection_query_results(
        _args(),
        command_name="watchtower-core query example",
        entries=("entry.example",),
        noun="example",
        empty_message="No example entries matched the requested filters.",
        payload_results_factory=lambda: (_ for _ in ()).throw(
            AssertionError("payload generation should stay lazy in human mode")
        ),
        render_entry=lambda entry: rendered.append(entry),
    )

    captured = capsys.readouterr()
    assert result == 0
    assert "Found 1 example entry:" in captured.out
    assert rendered == ["entry.example"]
