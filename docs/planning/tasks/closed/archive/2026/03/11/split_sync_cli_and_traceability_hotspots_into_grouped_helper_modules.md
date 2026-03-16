---
id: task.repo_local_hotspot_modularity.sync_traceability.001
trace_id: trace.repo_local_hotspot_modularity
title: Split sync CLI and traceability hotspots into grouped helper modules
summary: Reduce centralization in sync command registration, sync handlers, and traceability
  sync while preserving the durable sync command contract.
type: task
status: active
task_status: done
task_kind: chore
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T06:19:10Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/cli/sync_family.py
- core/python/src/watchtower_core/cli/sync_handlers.py
- core/python/src/watchtower_core/repo_ops/sync/traceability.py
- core/python/tests/
related_ids:
- prd.repo_local_hotspot_modularity
- design.features.repo_local_hotspot_modularity
- design.implementation.repo_local_hotspot_modularity
depends_on:
- task.repo_local_hotspot_modularity.bootstrap.001
---

# Split sync CLI and traceability hotspots into grouped helper modules

## Summary
Reduce centralization in sync command registration, sync handlers, and traceability sync while preserving the durable sync command contract.

## Scope
- Split sync-family parser registration into grouped helper builders while keeping register_sync_family as the stable entrypoint.
- Split sync runtime handlers and traceability sync helpers into smaller modules while preserving command payloads and sync outputs.

## Done When
- sync_family.py, sync_handlers.py, and traceability.py are materially smaller or thin facades backed by grouped helper modules.
- Sync CLI and traceability tests stay green with unchanged command behavior and output shapes.
