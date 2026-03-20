"""Compatibility shim for existing console-script environments."""

from __future__ import annotations

from watchtower_host.cli.main import main


if __name__ == "__main__":
    raise SystemExit(main())
