"""Compatibility facade for split query handler modules."""

from watchtower_core.cli.query_coordination_handlers import (
    _emit_initiative_query_results,
    _initiative_entry_payload,
    _run_query_coordination,
    _run_query_initiatives,
    _run_query_planning,
    _run_query_tasks,
    _run_query_trace,
)
from watchtower_core.cli.query_discovery_handlers import (
    _run_query_commands,
    _run_query_paths,
)
from watchtower_core.cli.query_knowledge_handlers import (
    _run_query_foundations,
    _run_query_references,
    _run_query_standards,
    _run_query_workflows,
)
from watchtower_core.cli.query_records_handlers import (
    _run_query_acceptance,
    _run_query_decisions,
    _run_query_designs,
    _run_query_evidence,
    _run_query_prds,
)

__all__ = [
    "_emit_initiative_query_results",
    "_initiative_entry_payload",
    "_run_query_acceptance",
    "_run_query_commands",
    "_run_query_coordination",
    "_run_query_decisions",
    "_run_query_designs",
    "_run_query_evidence",
    "_run_query_foundations",
    "_run_query_initiatives",
    "_run_query_planning",
    "_run_query_paths",
    "_run_query_prds",
    "_run_query_references",
    "_run_query_standards",
    "_run_query_tasks",
    "_run_query_trace",
    "_run_query_workflows",
]
