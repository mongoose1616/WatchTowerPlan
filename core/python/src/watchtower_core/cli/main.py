"""Compatibility wrapper around the host-owned CLI entrypoint."""

from __future__ import annotations

from watchtower_host.cli.main import main


if __name__ == "__main__":
    raise SystemExit(main())
