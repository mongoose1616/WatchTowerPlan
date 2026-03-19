from __future__ import annotations

import pytest

from watchtower_core.utils.module_exports import (
    fail_closed_package_getattr,
    lazy_module_getattr,
)


def test_lazy_module_getattr_resolves_known_exports_and_blocks_configured_names() -> None:
    getattr_fn = lazy_module_getattr(
        module_name="watchtower_core.test_exports",
        export_modules={"utc_timestamp_now": "watchtower_core.utils.timestamps"},
        blocked_messages={"RepoOnlySurface": "blocked for test"},
    )

    assert callable(getattr_fn("utc_timestamp_now"))

    with pytest.raises(AttributeError, match="blocked for test"):
        getattr_fn("RepoOnlySurface")


def test_lazy_module_getattr_fails_closed_for_unknown_names() -> None:
    getattr_fn = lazy_module_getattr(
        module_name="watchtower_core.test_exports",
        export_modules={},
    )

    with pytest.raises(AttributeError, match="watchtower_core.test_exports"):
        getattr_fn("UnknownSurface")


def test_fail_closed_package_getattr_raises_the_configured_message() -> None:
    getattr_fn = fail_closed_package_getattr("fail closed")

    with pytest.raises(AttributeError, match="fail closed"):
        getattr_fn("Anything")
