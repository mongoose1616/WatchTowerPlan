from __future__ import annotations

from watchtower_core.cli.main import main


def test_doctor_command_returns_zero(capsys) -> None:
    result = main(["doctor"])

    captured = capsys.readouterr()
    assert result == 0
    assert "workspace scaffold is available" in captured.out


def test_root_command_prints_help(capsys) -> None:
    result = main([])

    captured = capsys.readouterr()
    assert result == 0
    assert "watchtower-core" in captured.out
