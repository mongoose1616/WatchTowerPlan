"""Thin compatibility shim for environments with a stale console-script target."""

from __future__ import annotations

from watchtower_host.cli.main import main


if __name__ == "__main__":
    raise SystemExit(main())
