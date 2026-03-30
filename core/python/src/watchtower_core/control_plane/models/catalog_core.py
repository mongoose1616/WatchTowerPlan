"""Core catalog and validation-registry models."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.workspace import WorkspaceConfig


@dataclass(frozen=True, slots=True)
class SchemaCatalogRecord:
    """Catalog entry for a published schema."""

    schema_id: str
    title: str
    description: str
    status: str
    schema_family: str
    subject_kind: str
    version: str
    canonical_relative_path: str
    canonical_path: Path
    aliases: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(
        cls,
        document: dict[str, Any],
        workspace_config: WorkspaceConfig,
    ) -> SchemaCatalogRecord:
        return cls(
            schema_id=document["schema_id"],
            title=document["title"],
            description=document["description"],
            status=document["status"],
            schema_family=document["schema_family"],
            subject_kind=document["subject_kind"],
            version=document["version"],
            canonical_relative_path=document["canonical_path"],
            canonical_path=workspace_config.resolve_path(document["canonical_path"]),
            aliases=tuple(document.get("aliases", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class SchemaCatalog:
    """Typed schema-catalog artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    records: tuple[SchemaCatalogRecord, ...]

    @classmethod
    def from_document(
        cls,
        document: dict[str, Any],
        workspace_config: WorkspaceConfig,
    ) -> SchemaCatalog:
        records = tuple(
            SchemaCatalogRecord.from_document(record, workspace_config)
            for record in document["schemas"]
        )
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            records=records,
        )

    @classmethod
    def merge(cls, *catalogs: SchemaCatalog) -> SchemaCatalog:
        """Return one schema catalog with records combined in declaration order."""

        if not catalogs:
            raise ValueError("SchemaCatalog.merge requires at least one catalog.")

        primary = catalogs[0]
        merged_records: list[SchemaCatalogRecord] = []
        seen_schema_ids: set[str] = set()
        for catalog in catalogs:
            if catalog.schema_id != primary.schema_id:
                raise ValueError("Merged schema catalogs must share the same $schema value.")
            if catalog.artifact_id != primary.artifact_id:
                raise ValueError("Merged schema catalogs must share the same artifact ID.")
            for record in catalog.records:
                if record.schema_id in seen_schema_ids:
                    raise ValueError(
                        f"Merged schema catalogs contain duplicate schema IDs: {record.schema_id}"
                    )
                seen_schema_ids.add(record.schema_id)
                merged_records.append(record)

        return cls(
            schema_id=primary.schema_id,
            artifact_id=primary.artifact_id,
            title=primary.title,
            status=primary.status,
            records=tuple(merged_records),
        )

    def get(self, schema_id: str) -> SchemaCatalogRecord:
        """Return a catalog record by schema identifier."""
        for record in self.records:
            if record.schema_id == schema_id:
                return record
        raise KeyError(schema_id)

    def get_by_subject_kind(self, subject_kind: str) -> SchemaCatalogRecord:
        """Return the unique catalog record for one subject kind."""

        matches = tuple(record for record in self.records if record.subject_kind == subject_kind)
        if not matches:
            raise KeyError(subject_kind)
        if len(matches) > 1:
            raise ValueError(
                "Schema catalog subject kind must resolve to one record, "
                f"but {subject_kind!r} matched {len(matches)} entries."
            )
        return matches[0]


@dataclass(frozen=True, slots=True)
class ValidatorDefinition:
    """Validator registry entry."""

    validator_id: str
    title: str
    description: str
    status: str
    engine: str
    artifact_kind: str
    applies_to: tuple[str, ...]
    schema_ids: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ValidatorDefinition:
        return cls(
            validator_id=document["id"],
            title=document["title"],
            description=document["description"],
            status=document["status"],
            engine=document["engine"],
            artifact_kind=document["artifact_kind"],
            applies_to=tuple(document["applies_to"]),
            schema_ids=tuple(document.get("schema_ids", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class ValidatorRegistry:
    """Typed validator-registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    validators: tuple[ValidatorDefinition, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ValidatorRegistry:
        validators = tuple(
            ValidatorDefinition.from_document(entry) for entry in document["validators"]
        )
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            validators=validators,
        )

    @classmethod
    def merge(cls, *registries: ValidatorRegistry) -> ValidatorRegistry:
        """Return one validator registry with entries combined in declaration order."""

        if not registries:
            raise ValueError("ValidatorRegistry.merge requires at least one registry.")

        primary = registries[0]
        merged_validators: list[ValidatorDefinition] = []
        seen_validators: dict[str, ValidatorDefinition] = {}
        for registry in registries:
            if registry.schema_id != primary.schema_id:
                raise ValueError("Merged validator registries must share the same $schema value.")
            if registry.artifact_id != primary.artifact_id:
                raise ValueError("Merged validator registries must share the same artifact ID.")
            for validator in registry.validators:
                existing_validator = seen_validators.get(validator.validator_id)
                if existing_validator is not None:
                    if existing_validator != validator:
                        raise ValueError(
                            "Merged validator registries contain conflicting duplicate "
                            f"validator IDs: {validator.validator_id}"
                        )
                    continue
                seen_validators[validator.validator_id] = validator
                merged_validators.append(validator)

        return cls(
            schema_id=primary.schema_id,
            artifact_id=primary.artifact_id,
            title=primary.title,
            status=primary.status,
            validators=tuple(merged_validators),
        )

    def get(self, validator_id: str) -> ValidatorDefinition:
        """Return a validator definition by identifier."""
        for entry in self.validators:
            if entry.validator_id == validator_id:
                return entry
        raise KeyError(validator_id)


@dataclass(frozen=True, slots=True)
class ValidationSuiteStepDefinition:
    """Validation suite step definition."""

    step_id: str
    title: str
    description: str
    step_kind: str
    paths: tuple[str, ...] = ()
    validator_id: str | None = None
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ValidationSuiteStepDefinition:
        return cls(
            step_id=document["id"],
            title=document["title"],
            description=document["description"],
            step_kind=document["step_kind"],
            paths=tuple(document.get("paths", ())),
            validator_id=document.get("validator_id"),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class ValidationSuiteDefinition:
    """Validation suite definition."""

    suite_id: str
    title: str
    description: str
    status: str
    steps: tuple[ValidationSuiteStepDefinition, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ValidationSuiteDefinition:
        return cls(
            suite_id=document["id"],
            title=document["title"],
            description=document["description"],
            status=document["status"],
            steps=tuple(
                ValidationSuiteStepDefinition.from_document(entry) for entry in document["steps"]
            ),
            notes=document.get("notes"),
        )

    def get_step(self, step_id: str) -> ValidationSuiteStepDefinition:
        """Return one validation suite step by identifier."""

        for step in self.steps:
            if step.step_id == step_id:
                return step
        raise KeyError(step_id)


@dataclass(frozen=True, slots=True)
class ValidationSuiteRegistry:
    """Typed validation-suite registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    suites: tuple[ValidationSuiteDefinition, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ValidationSuiteRegistry:
        suites = tuple(
            ValidationSuiteDefinition.from_document(entry) for entry in document["suites"]
        )
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            suites=suites,
        )

    def get(self, suite_id: str) -> ValidationSuiteDefinition:
        """Return one validation suite by identifier."""

        for suite in self.suites:
            if suite.suite_id == suite_id:
                return suite
        raise KeyError(suite_id)


@dataclass(frozen=True, slots=True)
class BenchmarkSuiteCommandDefinition:
    """Benchmark-suite command definition."""

    command_id: str
    title: str
    description: str
    argv: tuple[str, ...]
    measured_runs_override: int | None = None
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> BenchmarkSuiteCommandDefinition:
        return cls(
            command_id=document["id"],
            title=document["title"],
            description=document["description"],
            argv=tuple(document["argv"]),
            measured_runs_override=document.get("measured_runs_override"),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class BenchmarkSuiteDefinition:
    """Benchmark suite definition."""

    suite_id: str
    title: str
    description: str
    status: str
    working_directory: str
    warmup_runs: int
    measured_runs: int
    commands: tuple[BenchmarkSuiteCommandDefinition, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> BenchmarkSuiteDefinition:
        return cls(
            suite_id=document["id"],
            title=document["title"],
            description=document["description"],
            status=document["status"],
            working_directory=document["working_directory"],
            warmup_runs=document["warmup_runs"],
            measured_runs=document["measured_runs"],
            commands=tuple(
                BenchmarkSuiteCommandDefinition.from_document(entry)
                for entry in document["commands"]
            ),
            notes=document.get("notes"),
        )

    def get_command(self, command_id: str) -> BenchmarkSuiteCommandDefinition:
        """Return one benchmark-suite command by identifier."""

        for command in self.commands:
            if command.command_id == command_id:
                return command
        raise KeyError(command_id)


@dataclass(frozen=True, slots=True)
class BenchmarkSuiteRegistry:
    """Typed benchmark-suite registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    suites: tuple[BenchmarkSuiteDefinition, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> BenchmarkSuiteRegistry:
        suites = tuple(
            BenchmarkSuiteDefinition.from_document(entry) for entry in document["suites"]
        )
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            suites=suites,
        )

    def get(self, suite_id: str) -> BenchmarkSuiteDefinition:
        """Return one benchmark suite by identifier."""

        for suite in self.suites:
            if suite.suite_id == suite_id:
                return suite
        raise KeyError(suite_id)
