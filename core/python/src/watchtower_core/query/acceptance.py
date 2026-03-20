"""Reusable query helpers for governed acceptance-contract artifacts."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import AcceptanceContract


@dataclass(frozen=True, slots=True)
class AcceptanceContractSearchParams:
    """Search filters for acceptance-contract lookups."""

    trace_id: str | None = None
    source_surface_path: str | None = None
    acceptance_id: str | None = None


class AcceptanceContractQueryService:
    """Search governed acceptance contracts."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def search(
        self,
        params: AcceptanceContractSearchParams,
    ) -> tuple[AcceptanceContract, ...]:
        """Return matching acceptance contracts."""

        results: list[AcceptanceContract] = []
        for contract in self._loader.load_acceptance_contracts():
            if params.trace_id is not None and contract.trace_id != params.trace_id:
                continue
            if (
                params.source_surface_path is not None
                and contract.source_surface_path != params.source_surface_path
            ):
                continue
            if params.acceptance_id is not None and not any(
                entry.acceptance_id == params.acceptance_id for entry in contract.entries
            ):
                continue
            results.append(contract)
        return tuple(results)


__all__ = ["AcceptanceContractQueryService", "AcceptanceContractSearchParams"]
