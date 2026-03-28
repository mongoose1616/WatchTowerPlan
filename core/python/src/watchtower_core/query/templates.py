"""Export-safe template-catalog query helpers."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import TemplateCatalog, TemplateCatalogEntry
from watchtower_core.query.common import query_score


@dataclass(frozen=True, slots=True)
class TemplateCatalogSearchParams:
    """Filter and ranking inputs for template-catalog lookup."""

    query: str | None = None
    template_id: str | None = None
    family_id: str | None = None
    surface_id: str | None = None
    authorship_mode: str | None = None
    llm_guidance_mode: str | None = None
    allowed_root: str | None = None
    required_section_id: str | None = None
    required_rendered_surface_id: str | None = None
    limit: int | None = None


class TemplateCatalogQueryService:
    """Search the governed template catalog for reusable document shapes."""

    def __init__(
        self,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> None:
        self._loader = loader
        self._pack_settings_path = pack_settings_path

    def search(
        self,
        params: TemplateCatalogSearchParams,
    ) -> tuple[TemplateCatalogEntry, ...]:
        """Return template entries matching the requested filters."""

        catalog = self._catalog()
        template_id = params.template_id.casefold() if params.template_id is not None else None
        family_id = params.family_id.casefold() if params.family_id is not None else None
        surface_id = params.surface_id.casefold() if params.surface_id is not None else None
        authorship_mode = (
            params.authorship_mode.casefold() if params.authorship_mode is not None else None
        )
        llm_guidance_mode = (
            params.llm_guidance_mode.casefold()
            if params.llm_guidance_mode is not None
            else None
        )
        allowed_root = params.allowed_root.casefold() if params.allowed_root is not None else None
        required_section_id = (
            params.required_section_id.casefold()
            if params.required_section_id is not None
            else None
        )
        required_rendered_surface_id = (
            params.required_rendered_surface_id.casefold()
            if params.required_rendered_surface_id is not None
            else None
        )

        matches: list[tuple[int, TemplateCatalogEntry]] = []
        for entry in catalog.entries:
            if template_id is not None and entry.template_id.casefold() != template_id:
                continue
            if family_id is not None and (entry.family_id or "").casefold() != family_id:
                continue
            if surface_id is not None and (entry.surface_id or "").casefold() != surface_id:
                continue
            if (
                authorship_mode is not None
                and entry.authorship_mode.casefold() != authorship_mode
            ):
                continue
            if (
                llm_guidance_mode is not None
                and entry.llm_guidance_mode.casefold() != llm_guidance_mode
            ):
                continue
            if allowed_root is not None and allowed_root not in {
                value.casefold() for value in entry.allowed_roots
            }:
                continue
            if required_section_id is not None and required_section_id not in {
                value.casefold() for value in entry.required_section_ids
            }:
                continue
            if required_rendered_surface_id is not None and required_rendered_surface_id not in {
                value.casefold() for value in entry.required_rendered_surface_ids
            }:
                continue

            guidance = entry.llm_guidance
            score = query_score(
                params.query,
                (
                    entry.template_id,
                    entry.family_id or "",
                    entry.surface_id or "",
                    entry.entry_status,
                    entry.authorship_mode,
                    entry.template_path,
                    entry.llm_guidance_mode,
                    entry.front_matter_schema_id or "",
                    entry.section_spec_schema_id or "",
                    guidance.authoring_goal if guidance is not None else "",
                    entry.operator_notes or "",
                    *entry.required_section_ids,
                    *entry.optional_section_ids,
                    *entry.section_order,
                    *entry.prohibited_section_ids,
                    *entry.allowed_roots,
                    *entry.required_rendered_surface_ids,
                    *(guidance.hard_requirements if guidance is not None else ()),
                    *(guidance.advisory_notes if guidance is not None else ()),
                ),
            )
            if score is None:
                continue
            matches.append((score, entry))

        matches.sort(key=lambda item: (-item[0], item[1].template_id))
        entries = [entry for _, entry in matches]
        if params.limit is not None:
            entries = entries[: params.limit]
        return tuple(entries)

    def _catalog(self) -> TemplateCatalog:
        effective_pack_settings_path = self._loader.effective_pack_settings_path(
            self._pack_settings_path
        )
        effective_loader = (
            self._loader
            if self._loader.active_pack_settings_path == effective_pack_settings_path
            else self._loader.derive(active_pack_settings_path=effective_pack_settings_path)
        )
        return effective_loader.load_template_catalog()


__all__ = ["TemplateCatalogQueryService", "TemplateCatalogSearchParams"]
