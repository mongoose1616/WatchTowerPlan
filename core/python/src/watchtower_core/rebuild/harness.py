"""Reusable rebuild-harness primitives for deterministic derived-surface generation."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.control_plane.workspace import (
    FileSystemArtifactIO,
    OverlayArtifactSource,
    WorkspaceConfig,
)

RebuildOutputFormat = Literal["json", "markdown"]
RebuildBuilder = Callable[[ControlPlaneLoader], tuple["RebuildOutput", ...]]


@dataclass(frozen=True, slots=True)
class RebuildOutput:
    """One derived output produced by a rebuild target."""

    relative_output_path: str
    artifact_kind: str
    output_format: RebuildOutputFormat
    content: dict[str, object] | str
    validated: bool = False


@dataclass(frozen=True, slots=True)
class RebuildTargetSpec:
    """One deterministic rebuild target included in aggregate orchestration."""

    target: str
    build_outputs: RebuildBuilder
    groups: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RebuildRecord:
    """One derived output written by the rebuild harness."""

    target: str
    artifact_kind: str
    relative_output_path: str
    output_format: RebuildOutputFormat
    output_path: str | None
    wrote: bool


@dataclass(frozen=True, slots=True)
class RebuildResult:
    """Aggregated output for one rebuild-harness run."""

    records: tuple[RebuildRecord, ...]
    wrote: bool
    output_dir: str | None


class RebuildHarness:
    """Reusable harness for deterministic derived-surface rebuilds."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> RebuildHarness:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def run_specs(
        self,
        specs: tuple[RebuildTargetSpec, ...],
        *,
        write: bool = False,
        output_dir: Path | None = None,
    ) -> RebuildResult:
        runtime_loader = self._runtime_loader(output_dir)
        records: list[RebuildRecord] = []
        seen_paths: set[str] = set()
        for spec in specs:
            for output in spec.build_outputs(runtime_loader):
                if output.relative_output_path in seen_paths:
                    raise ValueError(
                        "Rebuild targets produced the same output path more than once: "
                        f"{output.relative_output_path}"
                    )
                seen_paths.add(output.relative_output_path)
                records.append(
                    self._run_output(
                        loader=runtime_loader,
                        target=spec.target,
                        output=output,
                        write=write,
                        output_dir=output_dir,
                    )
                )
        return RebuildResult(
            records=tuple(records),
            wrote=(write or output_dir is not None),
            output_dir=str(output_dir.resolve()) if output_dir is not None else None,
        )

    def _run_output(
        self,
        *,
        loader: ControlPlaneLoader,
        target: str,
        output: RebuildOutput,
        write: bool,
        output_dir: Path | None,
    ) -> RebuildRecord:
        if output.output_format == "json":
            document = _require_json_document(output)
            if not output.validated:
                loader.schema_store.validate_instance(document)
            loader.set_validated_document_override(output.relative_output_path, document)
            destination = self._resolve_destination(output.relative_output_path, write, output_dir)
            wrote = destination is not None
            if destination is not None:
                if output_dir is None:
                    self._loader.artifact_store.write_json_object(
                        output.relative_output_path,
                        document,
                    )
                else:
                    self._loader.artifact_store.write_json_file(destination, document)
            return RebuildRecord(
                target=target,
                artifact_kind=output.artifact_kind,
                relative_output_path=output.relative_output_path,
                output_format=output.output_format,
                output_path=str(destination.resolve()) if destination is not None else None,
                wrote=wrote,
            )

        content = _require_markdown(output)
        destination = self._resolve_destination(output.relative_output_path, write, output_dir)
        wrote = destination is not None
        if destination is not None:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(f"{content.rstrip()}\n", encoding="utf-8")
        return RebuildRecord(
            target=target,
            artifact_kind=output.artifact_kind,
            relative_output_path=output.relative_output_path,
            output_format=output.output_format,
            output_path=str(destination.resolve()) if destination is not None else None,
            wrote=wrote,
        )

    def _resolve_destination(
        self,
        relative_output_path: str,
        write: bool,
        output_dir: Path | None,
    ) -> Path | None:
        if output_dir is not None:
            destination = output_dir / relative_output_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            return destination
        if not write:
            return None
        destination = self._repo_root / relative_output_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        return destination

    def _runtime_loader(self, output_dir: Path | None) -> ControlPlaneLoader:
        overlay_source = self._loader.artifact_source
        if output_dir is not None:
            overlay_workspace = WorkspaceConfig(
                repo_root=output_dir,
                control_plane_root=output_dir / "core" / "control_plane",
                python_workspace_root=output_dir / "core" / "python",
            )
            overlay_source = OverlayArtifactSource(
                primary=FileSystemArtifactIO(overlay_workspace),
                fallback=self._loader.artifact_source,
            )
        return ControlPlaneLoader(
            workspace_config=self._loader.workspace_config,
            schema_store=self._loader.schema_store,
            artifact_source=overlay_source,
            artifact_store=self._loader.artifact_store,
        )


def _require_json_document(output: RebuildOutput) -> dict[str, object]:
    if not isinstance(output.content, dict):
        raise TypeError(
            "JSON rebuild outputs must provide a dict document for "
            f"{output.relative_output_path}."
        )
    return output.content


def _require_markdown(output: RebuildOutput) -> str:
    if not isinstance(output.content, str):
        raise TypeError(
            "Markdown rebuild outputs must provide a string content payload for "
            f"{output.relative_output_path}."
        )
    return output.content


__all__ = [
    "RebuildBuilder",
    "RebuildHarness",
    "RebuildOutput",
    "RebuildOutputFormat",
    "RebuildRecord",
    "RebuildResult",
    "RebuildTargetSpec",
]
