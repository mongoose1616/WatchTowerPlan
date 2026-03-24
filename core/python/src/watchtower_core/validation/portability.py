"""Release and bootstrap portability validation over a repository root."""

from __future__ import annotations

import json
import os
import re
import tomllib
from pathlib import Path

from watchtower_core.validation.models import ValidationIssue, ValidationResult

_VALIDATOR_ID = "validator.portability.repository_export"
_ENGINE = "portability_scan"
_TEXT_SUFFIXES = {
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
_DEV_DIRECTORY_NAMES = {
    ".mypy_cache",
    ".nox",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "pip-wheel-metadata",
}
_DEV_FILE_NAMES = {
    ".coverage",
    "coverage.xml",
}
_DEV_FILE_SUFFIXES = (
    ".egg-link",
    ".pyc",
    ".pyo",
    ".whl",
)
_ABSOLUTE_PATH_PATTERNS = (
    re.compile(r"(?<![A-Za-z0-9_])/(?:home|Users|mnt|opt|private|srv|tmp|var)/[^\s`\"')]+"),
    re.compile(r"(?<![A-Za-z0-9_])[A-Za-z]:\\\\[^\s`\"')]+"),
)
_INTERNAL_REFERENCE_SUFFIXES = (
    "_assessment_closeout_reference.md",
    "_comparison_closeout_reference.md",
)
_NONPORTABLE_ACCEPTANCE_PATH_PREFIXES = (
    "core/control_plane/contracts/acceptance/",
    "core/control_plane/records/validation_evidence/",
)
REPOSITORY_EXPORT_SCOPE = "repository_bundle"
PACK_BUNDLE_EXPORT_SCOPE = "pack_bundle"


class PortabilityValidationService:
    """Validate that one repo root is scrubbed for release/bootstrap handoff."""

    def validate(
        self,
        root: str | Path,
        *,
        included_pack_slugs: tuple[str, ...] = (),
        scope: str = REPOSITORY_EXPORT_SCOPE,
    ) -> ValidationResult:
        root_path = Path(root).expanduser().resolve()
        if not root_path.exists():
            raise ValueError(f"Portability root does not exist: {root_path}")
        if not root_path.is_dir():
            raise ValueError(f"Portability root must be a directory: {root_path}")

        normalized_pack_slugs = tuple(dict.fromkeys(included_pack_slugs))
        if scope not in {REPOSITORY_EXPORT_SCOPE, PACK_BUNDLE_EXPORT_SCOPE}:
            raise ValueError(f"Unknown portability scope: {scope}")
        if scope == PACK_BUNDLE_EXPORT_SCOPE and not normalized_pack_slugs:
            raise ValueError(
                "Pack-bundle portability validation requires at least one --include-pack slug."
            )

        issues = (
            self._scan_retained_history(root_path)
            + self._scan_acceptance_lineage(root_path)
            + self._scan_developer_residue(root_path)
            + self._scan_pack_runtime_state(root_path)
            + self._scan_test_surfaces(root_path)
            + self._scan_project_repository_maps(root_path)
            + self._scan_internal_assessment_documents(root_path)
            + self._scan_absolute_paths(root_path)
        )
        if scope == REPOSITORY_EXPORT_SCOPE:
            issues.extend(self._scan_pack_selection(root_path, normalized_pack_slugs))
        else:
            issues.extend(self._scan_pack_bundle_selection(root_path, normalized_pack_slugs))
        issues = sorted(
            issues,
            key=lambda issue: (issue.location or "", issue.code, issue.message),
        )
        return ValidationResult(
            validator_id=_VALIDATOR_ID,
            target_path=str(root_path),
            engine=_ENGINE,
            schema_ids=(),
            passed=not issues,
            issues=tuple(issues),
        )

    def _scan_retained_history(self, root_path: Path) -> list[ValidationIssue]:
        records_root = root_path / "core" / "control_plane" / "records"
        if not records_root.exists():
            return []

        issues: list[ValidationIssue] = []
        for child in sorted(records_root.iterdir()):
            if not self._contains_retained_history(child):
                continue
            issues.append(
                ValidationIssue(
                    code="retained_history_present",
                    message=(
                        "Customer-ready exports must exclude retained control-plane history "
                        f"surfaces such as {self._relative(child, root_path)}."
                    ),
                    location=self._relative(child, root_path),
                )
            )
        return issues

    def _scan_acceptance_lineage(self, root_path: Path) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        acceptance_root = root_path / "core" / "control_plane" / "contracts" / "acceptance"
        if acceptance_root.exists():
            for candidate in sorted(acceptance_root.glob("*.json")):
                issues.append(
                    ValidationIssue(
                        code="acceptance_contract_present",
                        message=(
                            "Customer-ready exports must exclude shared acceptance-contract "
                            f"artifacts such as {self._relative(candidate, root_path)} because "
                            "portable bundles omit the retained evidence needed to reconcile "
                            "them."
                        ),
                        location=self._relative(candidate, root_path),
                    )
                )

        traceability_path = (
            root_path / "core" / "control_plane" / "indexes" / "traceability"
            / "traceability_index.json"
        )
        if not traceability_path.exists():
            return issues

        try:
            document = json.loads(traceability_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return issues

        for entry in document.get("entries", ()):
            if not traceability_entry_requires_nonportable_acceptance_lineage(entry):
                continue
            trace_id = entry.get("trace_id") if isinstance(entry, dict) else None
            trace_label = trace_id if isinstance(trace_id, str) else "<unknown-trace>"
            issues.append(
                ValidationIssue(
                    code="traceability_acceptance_lineage_present",
                    message=(
                        "Customer-ready exports must exclude acceptance-linked traceability "
                        f"lineage such as {trace_label} because the paired acceptance "
                        "contracts and retained evidence are internal-only surfaces."
                    ),
                    location=self._relative(traceability_path, root_path),
                )
            )
        return issues

    def _contains_retained_history(self, candidate: Path) -> bool:
        if candidate.is_file():
            return candidate.name != "README.md"
        if not candidate.is_dir():
            return False
        return any(
            path.is_file() and path.name != "README.md" for path in candidate.rglob("*")
        )

    def _scan_developer_residue(self, root_path: Path) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for current_root, dirnames, filenames in os.walk(root_path, topdown=True):
            current_path = Path(current_root)
            dirnames[:] = sorted(dirname for dirname in dirnames if dirname != ".git")

            removable_dirs = tuple(
                dirname for dirname in dirnames if dirname in _DEV_DIRECTORY_NAMES
            )
            for dirname in removable_dirs:
                issues.append(
                    ValidationIssue(
                        code="developer_residue_present",
                        message=(
                            "Customer-ready exports must exclude developer-machine residue such "
                            f"as {self._relative(current_path / dirname, root_path)}."
                        ),
                        location=self._relative(current_path / dirname, root_path),
                    )
                )
            dirnames[:] = [dirname for dirname in dirnames if dirname not in _DEV_DIRECTORY_NAMES]

            for filename in sorted(filenames):
                path = current_path / filename
                relative_path = self._relative(path, root_path)
                if filename in _DEV_FILE_NAMES or filename.endswith(_DEV_FILE_SUFFIXES):
                    issues.append(
                        ValidationIssue(
                            code="developer_residue_present",
                            message=(
                                "Customer-ready exports must exclude developer-machine residue "
                                f"such as {relative_path}."
                            ),
                            location=relative_path,
                        )
                    )
                elif filename.endswith(".egg-info"):
                    issues.append(
                        ValidationIssue(
                            code="developer_residue_present",
                            message=(
                                "Customer-ready exports must exclude editable-install metadata "
                                f"such as {relative_path}."
                            ),
                            location=relative_path,
                        )
                    )
        return issues

    def _scan_pack_runtime_state(self, root_path: Path) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for candidate in sorted(root_path.rglob("runtime")):
            if not candidate.is_dir() or candidate.parent.name != ".wt":
                continue
            if not any(candidate.iterdir()):
                continue
            issues.append(
                ValidationIssue(
                    code="pack_runtime_state_present",
                    message=(
                        "Customer-ready exports must exclude pack-local runtime state such as "
                        f"{self._relative(candidate, root_path)}."
                    ),
                    location=self._relative(candidate, root_path),
                )
            )
        return issues

    def _scan_test_surfaces(self, root_path: Path) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        test_roots = {
            candidate for candidate in root_path.rglob("python/tests") if candidate.is_dir()
        }
        for candidate in sorted(test_roots):
            if not any(candidate.iterdir()):
                continue
            issues.append(
                ValidationIssue(
                    code="test_surface_present",
                    message=(
                        "Customer-ready exports must exclude shared and pack-owned test "
                        f"trees such as {self._relative(candidate, root_path)}."
                    ),
                    location=self._relative(candidate, root_path),
                )
            )
        for candidate in sorted(root_path.rglob("testing")):
            if (
                not candidate.is_dir()
                or candidate.parent.parent.name != "src"
                or not candidate.parent.name.startswith("watchtower_")
                or not any(candidate.iterdir())
            ):
                continue
            issues.append(
                ValidationIssue(
                    code="pack_testing_module_present",
                    message=(
                        "Customer-ready exports must exclude pack-owned testing helper "
                        f"modules such as {self._relative(candidate, root_path)}."
                    ),
                    location=self._relative(candidate, root_path),
                )
            )
        return issues

    def _scan_project_repository_maps(self, root_path: Path) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for candidate in sorted(root_path.rglob("project_repository_map.json")):
            if not candidate.is_file():
                continue
            issues.append(
                ValidationIssue(
                    code="donor_project_map_present",
                    message=(
                        "Customer-ready exports must exclude donor project repository maps such "
                        f"as {self._relative(candidate, root_path)}."
                    ),
                    location=self._relative(candidate, root_path),
                )
            )
        return issues

    def _scan_pack_selection(
        self,
        root_path: Path,
        included_pack_slugs: tuple[str, ...],
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        included_set = set(included_pack_slugs)
        pack_registry_path = (
            root_path / "core" / "control_plane" / "registries" / "pack_registry.json"
        )
        registry_entries = self._load_pack_registry_entries(pack_registry_path)
        registry_pack_slugs = {entry["pack_slug"] for entry in registry_entries}

        for entry in registry_entries:
            pack_slug = entry["pack_slug"]
            pack_root = entry["pack_root"]
            if pack_slug not in included_set:
                issues.append(
                    ValidationIssue(
                        code="omitted_pack_registry_entry",
                        message=(
                            "Shared pack registry still declares omitted hosted pack "
                            f"{pack_slug!r}; bootstrap exports must reconcile the registry to "
                            "exactly the selected pack set."
                        ),
                        location=self._relative(pack_registry_path, root_path),
                    )
                )
                candidate_root = root_path / pack_root
                if candidate_root.exists():
                    issues.append(
                        ValidationIssue(
                            code="omitted_pack_root_present",
                            message=(
                                "Customer-ready exports must exclude omitted hosted pack roots "
                                f"such as {self._relative(candidate_root, root_path)}."
                            ),
                            location=self._relative(candidate_root, root_path),
                        )
                    )

        for pack_slug in included_pack_slugs:
            if pack_slug not in registry_pack_slugs:
                issues.append(
                    ValidationIssue(
                        code="selected_pack_missing",
                        message=(
                            f"Selected hosted pack {pack_slug!r} is missing from the shared pack "
                            "registry for the target root."
                        ),
                        location=self._relative(pack_registry_path, root_path)
                        if pack_registry_path.exists()
                        else "core/control_plane/registries/pack_registry.json",
                    )
                )

        issues.extend(
            self._scan_core_workspace_pack_references(
                root_path,
                registry_entries,
                included_set,
            )
        )
        return issues

    def _scan_pack_bundle_selection(
        self,
        root_path: Path,
        included_pack_slugs: tuple[str, ...],
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        included_set = set(included_pack_slugs)
        discovered_entries = self._discover_pack_bundle_entries(root_path)
        discovered_pack_slugs = {entry["pack_slug"] for entry in discovered_entries}

        core_root = root_path / "core"
        if core_root.exists():
            issues.append(
                ValidationIssue(
                    code="shared_core_surface_present",
                    message=(
                        "Pack-only exports must exclude shared core surfaces such as core/. "
                        "Export core separately or validate this root as a repository bundle "
                        "instead."
                    ),
                    location="core",
                )
            )

        for entry in discovered_entries:
            pack_slug = entry["pack_slug"]
            workspace_root = entry["workspace_root"]
            if pack_slug in included_set:
                continue
            issues.append(
                ValidationIssue(
                    code="omitted_pack_root_present",
                    message=(
                        "Pack-only exports must exclude omitted hosted pack roots such as "
                        f"{workspace_root}."
                    ),
                    location=workspace_root,
                )
            )

        for pack_slug in included_pack_slugs:
            if pack_slug in discovered_pack_slugs:
                continue
            issues.append(
                ValidationIssue(
                    code="selected_pack_missing",
                    message=(
                        f"Selected hosted pack {pack_slug!r} is missing from the pack-only "
                        "export root."
                    ),
                    location=".",
                )
            )

        return issues

    def _scan_core_workspace_pack_references(
        self,
        root_path: Path,
        registry_entries: list[dict[str, str]],
        included_pack_slugs: set[str],
    ) -> list[ValidationIssue]:
        pyproject_path = root_path / "core" / "python" / "pyproject.toml"
        if not pyproject_path.exists():
            return []

        document = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
        issues: list[ValidationIssue] = []
        distribution_to_slug = {
            entry["python_distribution"]: entry["pack_slug"] for entry in registry_entries
        }

        dev_dependencies = tuple(
            document.get("project", {}).get("optional-dependencies", {}).get("dev", ())
        )
        for dependency in dev_dependencies:
            pack_slug = distribution_to_slug.get(dependency)
            if pack_slug is None or pack_slug in included_pack_slugs:
                continue
            issues.append(
                ValidationIssue(
                    code="workspace_pack_dependency_present",
                    message=(
                        "Shared core workspace still declares omitted hosted pack dependency "
                        f"{dependency!r} for pack {pack_slug!r}."
                    ),
                    location=self._relative(pyproject_path, root_path),
                )
            )

        uv_sources = document.get("tool", {}).get("uv", {}).get("sources", {})
        for distribution, source in sorted(uv_sources.items()):
            if not isinstance(source, dict):
                continue
            raw_path = source.get("path")
            if not isinstance(raw_path, str):
                continue
            pack_root = self._resolve_relative_source_root(
                pyproject_path.parent,
                raw_path,
                root_path,
            )
            if pack_root is None:
                continue
            pack_slug = distribution_to_slug.get(distribution, pack_root)
            if pack_slug in included_pack_slugs:
                continue
            issues.append(
                ValidationIssue(
                    code="workspace_pack_source_present",
                    message=(
                        "Shared core workspace still points at omitted hosted pack source "
                        f"{pack_slug!r} through {raw_path!r}."
                    ),
                    location=self._relative(pyproject_path, root_path),
                )
            )
        return issues

    def _scan_absolute_paths(self, root_path: Path) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for path in self._iter_text_files(root_path):
            text = path.read_text(encoding="utf-8", errors="ignore")
            match = self._first_absolute_path_match(text)
            if match is None:
                continue
            issues.append(
                ValidationIssue(
                    code="absolute_donor_path_present",
                    message=(
                        "Portable outputs must use repository-relative paths or neutral "
                        f"placeholders, not filesystem-absolute paths such as {match!r}."
                    ),
                    location=self._relative(path, root_path),
                )
            )
        return issues

    def _scan_internal_assessment_documents(self, root_path: Path) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for candidate in sorted(root_path.rglob("*.md")):
            if not candidate.is_file():
                continue
            relative_path = candidate.relative_to(root_path).as_posix()
            if "docs/references/" not in relative_path:
                continue
            if not candidate.name.endswith(_INTERNAL_REFERENCE_SUFFIXES):
                continue
            issues.append(
                ValidationIssue(
                    code="internal_assessment_document_present",
                    message=(
                        "Customer-ready exports must exclude donor-only assessment or "
                        f"comparison closeout references such as {relative_path}."
                    ),
                    location=relative_path,
                )
            )
        return issues

    def _iter_text_files(self, root_path: Path) -> tuple[Path, ...]:
        files: list[Path] = []
        for current_root, dirnames, filenames in os.walk(root_path, topdown=True):
            current_path = Path(current_root)
            dirnames[:] = sorted(
                dirname
                for dirname in dirnames
                if dirname not in _DEV_DIRECTORY_NAMES and dirname != ".git"
            )
            for filename in sorted(filenames):
                path = current_path / filename
                if self._is_internal_test_surface(path, root_path):
                    continue
                if path.suffix.lower() not in _TEXT_SUFFIXES:
                    continue
                files.append(path)
        return tuple(files)

    def _first_absolute_path_match(self, text: str) -> str | None:
        for pattern in _ABSOLUTE_PATH_PATTERNS:
            match = pattern.search(text)
            if match is not None:
                candidate = match.group(0)
                if self._is_neutral_placeholder_path(candidate):
                    continue
                return candidate
        return None

    def _is_internal_test_surface(self, path: Path, root_path: Path) -> bool:
        relative_parts = path.relative_to(root_path).parts
        if relative_parts[:3] == ("core", "python", "tests"):
            return True
        if len(relative_parts) >= 3 and relative_parts[1:3] == ("python", "tests"):
            return True
        return (
            len(relative_parts) >= 5
            and relative_parts[1:3] == ("python", "src")
            and relative_parts[3].startswith("watchtower_")
            and relative_parts[4] == "testing"
        )

    def _is_neutral_placeholder_path(self, candidate: str) -> bool:
        return (
            candidate.startswith("/tmp/")
            or candidate.startswith("/private/tmp/")
            or candidate.startswith("/home/...")
            or candidate.startswith("C:\\...")
            or "..." in candidate
        )

    def _load_pack_registry_entries(self, pack_registry_path: Path) -> list[dict[str, str]]:
        if not pack_registry_path.exists():
            return []
        document = json.loads(pack_registry_path.read_text(encoding="utf-8"))
        entries: list[dict[str, str]] = []
        for entry in document.get("packs", ()):
            pack_slug = entry.get("pack_slug")
            pack_settings_path = entry.get("pack_settings_path")
            python_distribution = entry.get("python_distribution")
            if not isinstance(pack_slug, str) or not isinstance(pack_settings_path, str):
                continue
            pack_root = pack_settings_path.split("/", 1)[0]
            entries.append(
                {
                    "pack_slug": pack_slug,
                    "pack_root": pack_root,
                    "python_distribution": (
                        python_distribution if isinstance(python_distribution, str) else pack_slug
                    ),
                }
            )
        return entries

    def _discover_pack_bundle_entries(self, root_path: Path) -> list[dict[str, str]]:
        entries: list[dict[str, str]] = []
        for manifest_path in sorted(root_path.rglob("pack_runtime_manifest.json")):
            if (
                manifest_path.parent.name != "manifests"
                or manifest_path.parent.parent.name != ".wt"
            ):
                continue
            document = json.loads(manifest_path.read_text(encoding="utf-8"))
            pack_slug = document.get("pack_slug")
            owned_roots = document.get("owned_roots", {})
            workspace_root = owned_roots.get("workspace_root")
            if not isinstance(pack_slug, str) or not isinstance(workspace_root, str):
                continue
            entries.append(
                {
                    "pack_slug": pack_slug,
                    "workspace_root": workspace_root,
                }
            )
        return entries

    def _resolve_relative_source_root(
        self,
        base_dir: Path,
        raw_path: str,
        root_path: Path,
    ) -> str | None:
        candidate = (base_dir / raw_path).resolve()
        try:
            relative = candidate.relative_to(root_path)
        except ValueError:
            return None
        return relative.parts[0] if relative.parts else None

    def _relative(self, path: Path, root_path: Path) -> str:
        return path.relative_to(root_path).as_posix()


def traceability_entry_requires_nonportable_acceptance_lineage(entry: object) -> bool:
    if not isinstance(entry, dict):
        return False

    for key in ("acceptance_ids", "acceptance_contract_ids", "evidence_ids"):
        value = entry.get(key)
        if isinstance(value, list) and value:
            return True

    for key in ("source_surface_paths", "related_paths"):
        values = entry.get(key)
        if not isinstance(values, list):
            continue
        if any(
            isinstance(value, str)
            and value.startswith(_NONPORTABLE_ACCEPTANCE_PATH_PREFIXES)
            for value in values
        ):
            return True
    return False


__all__ = [
    "PACK_BUNDLE_EXPORT_SCOPE",
    "PortabilityValidationService",
    "REPOSITORY_EXPORT_SCOPE",
]
