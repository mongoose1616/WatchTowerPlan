from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.loader import CORE_PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.query import (
    AuthorityMapQueryService,
    AuthorityMapSearchParams,
    TemplateCatalogQueryService,
    TemplateCatalogSearchParams,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_authority_query_service_supports_exact_filters() -> None:
    service = AuthorityMapQueryService(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=CORE_PACK_SETTINGS_PATH,
    )

    entries = service.search(
        AuthorityMapSearchParams(
            question_id="authority.governance.template_selection",
        )
    )

    assert [entry.question_id for entry in entries] == [
        "authority.governance.template_selection"
    ]
    assert entries[0].preferred_command == "watchtower-core query templates"


def test_authority_query_service_ranks_lookup_discipline_queries() -> None:
    service = AuthorityMapQueryService(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=CORE_PACK_SETTINGS_PATH,
    )

    entries = service.search(AuthorityMapSearchParams(query="canonical lookup order"))

    assert entries
    assert entries[0].question_id == "authority.governance.lookup_discipline"


def test_authority_query_service_returns_empty_tuple_for_missing_question() -> None:
    service = AuthorityMapQueryService(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=CORE_PACK_SETTINGS_PATH,
    )

    entries = service.search(
        AuthorityMapSearchParams(question_id="authority.governance.missing")
    )

    assert entries == ()


def test_template_catalog_query_service_supports_exact_filters() -> None:
    service = TemplateCatalogQueryService(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=CORE_PACK_SETTINGS_PATH,
    )

    entries = service.search(
        TemplateCatalogSearchParams(
            template_id="template.core.documentation.standard",
        )
    )

    assert [entry.template_id for entry in entries] == [
        "template.core.documentation.standard"
    ]
    assert entries[0].template_path == "core/docs/templates/standard_document_template.md"


def test_template_catalog_query_service_ranks_reference_queries() -> None:
    service = TemplateCatalogQueryService(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=CORE_PACK_SETTINGS_PATH,
    )

    entries = service.search(
        TemplateCatalogSearchParams(query="canonical upstream distilled reference")
    )

    assert entries
    assert entries[0].template_id == "template.core.documentation.reference"


def test_template_catalog_query_service_supports_structured_filters() -> None:
    service = TemplateCatalogQueryService(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=CORE_PACK_SETTINGS_PATH,
    )

    entries = service.search(
        TemplateCatalogSearchParams(
            allowed_root="core/docs/commands",
            required_section_id="command",
        )
    )

    assert [entry.template_id for entry in entries] == [
        "template.core.documentation.command_reference"
    ]


def test_template_catalog_query_service_returns_empty_tuple_for_missing_surface() -> None:
    service = TemplateCatalogQueryService(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=CORE_PACK_SETTINGS_PATH,
    )

    entries = service.search(
        TemplateCatalogSearchParams(surface_id="surface.documentation.missing")
    )

    assert entries == ()
