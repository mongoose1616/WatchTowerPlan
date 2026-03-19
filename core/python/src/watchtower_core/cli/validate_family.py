"""Validate command-family registration."""

from __future__ import annotations

import argparse
from textwrap import dedent

from watchtower_core.cli.common import (
    HelpFormatter,
    add_common_validation_arguments,
    add_human_json_format_argument,
    add_pack_settings_argument,
    examples,
)


def register_validate_family(
    subparsers: argparse._SubParsersAction,
) -> None:
    """Register the validate command family and its subcommands."""
    from watchtower_core.cli.handler_common import _run_help
    from watchtower_core.cli.validation_handlers import (
        _run_validate_acceptance,
        _run_validate_all,
        _run_validate_artifact,
        _run_validate_document_semantics,
        _run_validate_front_matter,
        _run_validate_suite,
    )

    validate_parser = subparsers.add_parser(
        "validate",
        help="Run governed validation commands.",
        description=dedent(
            """
            Run validation commands against governed repository artifacts and
            document surfaces.

            Use `all` for one bounded repo-wide validation pass, `suite` for a
            pack-declared validation suite, `front-matter` for governed
            Markdown metadata, `document-semantics` for governed
            document-shape and applied-reference rules, `artifact` for
            schema-backed JSON contracts, indexes, ledgers, and similar
            machine-readable artifacts, and `acceptance` for semantic reconciliation across PRDs,
            acceptance contracts, validation evidence, and traceability.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core validate all --skip-acceptance",
            "uv run watchtower-core validate all --format json",
            "uv run watchtower-core validate suite --suite-id "
            "suite.watchtower_plan.validation_baseline --format json",
            "uv run watchtower-core validate front-matter --path "
            "core/docs/references/front_matter_reference.md",
            "uv run watchtower-core validate document-semantics --path "
            "core/workflows/modules/code_validation.md",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/contracts/acceptance/"
            "governed_acceptance_example_acceptance.json",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/indexes/traceability/traceability_index.json "
            "--format json",
            "uv run watchtower-core validate acceptance --trace-id "
            "trace.governed_acceptance_example --format json",
            "uv run watchtower-core validate front-matter --path "
            "core/docs/standards/metadata/front_matter_standard.md --format json",
        ),
        formatter_class=HelpFormatter,
    )
    validate_subparsers = validate_parser.add_subparsers(
        dest="validate_command",
        title="validate commands",
        metavar="<validate_command>",
    )
    validate_parser.set_defaults(handler=_run_help, help_parser=validate_parser)

    validate_all_parser = validate_subparsers.add_parser(
        "all",
        help="Run the current explicit validation families across governed repository surfaces.",
        description=dedent(
            """
            Run the current explicit validation families across the governed
            repository surfaces in deterministic order.

            This command is read-only. It aggregates front-matter validation,
            document-semantic validation, schema-backed artifact validation
            across live governed artifacts and canonical valid examples, and
            acceptance reconciliation so you can get one bounded validation
            summary without invoking each family manually.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core validate all --skip-acceptance",
            "uv run watchtower-core validate all --format json",
            "uv run watchtower-core validate all --skip-front-matter "
            "--skip-document-semantics --skip-artifacts",
        ),
        formatter_class=HelpFormatter,
    )
    validate_all_parser.add_argument(
        "--skip-front-matter",
        action="store_true",
        help="Skip governed Markdown front-matter validation targets.",
    )
    validate_all_parser.add_argument(
        "--skip-document-semantics",
        action="store_true",
        help="Skip governed document semantic validation targets.",
    )
    validate_all_parser.add_argument(
        "--skip-artifacts",
        action="store_true",
        help="Skip schema-backed governed JSON artifact validation targets.",
    )
    validate_all_parser.add_argument(
        "--skip-acceptance",
        action="store_true",
        help="Skip trace-level acceptance reconciliation checks.",
    )
    add_human_json_format_argument(validate_all_parser)
    validate_all_parser.set_defaults(handler=_run_validate_all)

    validate_suite_parser = validate_subparsers.add_parser(
        "suite",
        help="Run one pack-declared validation suite through reusable-core orchestration.",
        description=dedent(
            """
            Run one validation suite declared in the active validation-suite
            registry for the selected pack settings surface.

            Use this when you want reusable-core orchestration over a pack's
            declared validation steps rather than invoking each validation
            family manually.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core validate suite --suite-id "
            "suite.watchtower_plan.validation_baseline",
            "uv run watchtower-core validate suite --suite-id "
            "suite.plan.validation_baseline --pack-settings-path "
            "packs/plan/.wt/pack_settings.json --format json",
        ),
        formatter_class=HelpFormatter,
    )
    validate_suite_parser.add_argument(
        "--suite-id",
        required=True,
        help=(
            "Stable validation suite identifier such as "
            "suite.watchtower_plan.validation_baseline."
        ),
    )
    add_pack_settings_argument(validate_suite_parser)
    add_human_json_format_argument(validate_suite_parser)
    validate_suite_parser.set_defaults(handler=_run_validate_suite)

    validate_front_matter_parser = validate_subparsers.add_parser(
        "front-matter",
        help="Validate one Markdown document front-matter block.",
        description=dedent(
            """
            Validate one Markdown document front-matter block against the
            governed front-matter profiles published in the control plane.

            The command auto-selects the validator from the registry when the
            path is repository-local, or you can provide `--validator-id`
            explicitly.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core validate front-matter --path "
            "core/docs/references/front_matter_reference.md",
            "uv run watchtower-core validate front-matter --path "
            "core/docs/standards/metadata/front_matter_standard.md --format json",
            "uv run watchtower-core validate front-matter --path /tmp/example.md "
            "--validator-id validator.documentation.standard_front_matter",
            "uv run watchtower-core validate front-matter --path "
            "core/docs/standards/metadata/front_matter_standard.md --record-evidence "
            "--trace-id trace.governed_acceptance_example",
        ),
        formatter_class=HelpFormatter,
    )
    validate_front_matter_parser.add_argument(
        "--path",
        required=True,
        help="Repository-relative or absolute path to the Markdown document to validate.",
    )
    validate_front_matter_parser.add_argument(
        "--validator-id",
        help=(
            "Optional explicit validator identifier. Required for files outside "
            "the repository tree."
        ),
    )
    add_pack_settings_argument(validate_front_matter_parser)
    add_common_validation_arguments(validate_front_matter_parser)
    validate_front_matter_parser.set_defaults(handler=_run_validate_front_matter)

    validate_document_semantics_parser = validate_subparsers.add_parser(
        "document-semantics",
        help="Validate one governed Markdown document against repo-native semantic rules.",
        description=dedent(
            """
            Validate one governed Markdown document against the repository's
            semantic document rules, such as required sections, section order,
            applied-reference explanation rules, and family-specific guardrails.

            The command auto-selects the validator from the registry when the
            path is repository-local, or you can provide `--validator-id`
            explicitly.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core validate document-semantics --path "
            "core/docs/standards/documentation/workflow_md_standard.md",
            "uv run watchtower-core validate document-semantics --path "
            "core/workflows/modules/code_validation.md --format json",
            "uv run watchtower-core validate document-semantics --path "
            "/tmp/example.md --validator-id validator.documentation.standard_semantics",
        ),
        formatter_class=HelpFormatter,
    )
    validate_document_semantics_parser.add_argument(
        "--path",
        required=True,
        help="Repository-relative or absolute path to the Markdown document to validate.",
    )
    validate_document_semantics_parser.add_argument(
        "--validator-id",
        help=(
            "Optional explicit validator identifier. Required for files outside "
            "the repository tree."
        ),
    )
    add_pack_settings_argument(validate_document_semantics_parser)
    add_common_validation_arguments(validate_document_semantics_parser)
    validate_document_semantics_parser.set_defaults(handler=_run_validate_document_semantics)

    validate_artifact_parser = validate_subparsers.add_parser(
        "artifact",
        help="Validate one governed JSON artifact against registry-backed schema validators.",
        description=dedent(
            """
            Validate one governed JSON artifact against the active schema-backed
            validators published in the control plane.

            The command auto-selects the validator from the registry when the
            path is repository-local. For external or temporary files, you can
            provide `--validator-id`, validate directly against `--schema-id`,
            or rely on a document `$schema` plus supplemental schema paths.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/contracts/acceptance/"
            "governed_acceptance_example_acceptance.json",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/indexes/traceability/traceability_index.json "
            "--format json",
            "uv run watchtower-core validate artifact --path /tmp/example.json "
            "--validator-id validator.control_plane.acceptance_contract",
            "uv run watchtower-core validate artifact --path /tmp/pack_note.json "
            "--schema-id urn:watchtower:schema:external:pack-note:v1 "
            "--supplemental-schema-path /tmp/pack_schemas",
            "uv run watchtower-core validate artifact --path /tmp/pack_note.json "
            "--supplemental-schema-path /tmp/pack_schemas --format json",
            "uv run watchtower-core validate artifact --path "
            "core/control_plane/contracts/acceptance/"
            "governed_acceptance_example_acceptance.json "
            "--record-evidence --trace-id "
            "trace.governed_acceptance_example",
        ),
        formatter_class=HelpFormatter,
    )
    validate_artifact_parser.add_argument(
        "--path",
        required=True,
        help="Repository-relative or absolute path to the JSON artifact to validate.",
    )
    validator_selection_group = validate_artifact_parser.add_mutually_exclusive_group()
    validator_selection_group.add_argument(
        "--validator-id",
        help=(
            "Optional explicit validator identifier. Use this to force one "
            "registry-backed validator."
        ),
    )
    validator_selection_group.add_argument(
        "--schema-id",
        help=(
            "Optional direct schema identifier. Use this to validate against a "
            "cataloged or supplemental schema without selecting a registry validator."
        ),
    )
    validate_artifact_parser.add_argument(
        "--supplemental-schema-path",
        action="append",
        default=[],
        help=(
            "Optional repository-relative or absolute path to one supplemental "
            "schema file or directory. Repeat for multiple locations."
        ),
    )
    add_pack_settings_argument(validate_artifact_parser)
    add_common_validation_arguments(validate_artifact_parser)
    validate_artifact_parser.set_defaults(handler=_run_validate_artifact)

    validate_acceptance_parser = validate_subparsers.add_parser(
        "acceptance",
        help="Validate one trace across acceptance contracts, evidence, and traceability.",
        description=dedent(
            """
            Validate one traced initiative across trace-level acceptance IDs,
            acceptance contracts, validation evidence, validator references,
            source-surface links, and the traceability index.

            Use this when you need semantic acceptance reconciliation rather
            than only schema validation.
            """
        ).strip(),
        epilog=examples(
            "uv run watchtower-core validate acceptance --trace-id "
            "trace.governed_acceptance_example",
            "uv run watchtower-core validate acceptance --trace-id "
            "trace.governed_acceptance_example --format json",
        ),
        formatter_class=HelpFormatter,
    )
    validate_acceptance_parser.add_argument(
        "--trace-id",
        required=True,
        help="Stable trace identifier such as trace.governed_acceptance_example.",
    )
    add_human_json_format_argument(validate_acceptance_parser)
    validate_acceptance_parser.set_defaults(handler=_run_validate_acceptance)
