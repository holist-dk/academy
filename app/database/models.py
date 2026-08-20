"""
SQLAlchemy table definitions.

Organized into three layers per ADR-009 (docs/adr/ADR-009-database-persistence-model.md):

1. Institutional History - EvidenceEntry. One row per entry, append-only
   (UPDATE/DELETE revoked at the database permission level).
2. Current Institutional State - LearnerModel, KnowledgeMap, Identity,
   Facts, Metadata. Ordinary mutable tables, current values only - no
   history of previous values (see ADR-009's Known Accepted Gap).
3. Active Session - persisted for crash recovery only. Cache/infrastructure
   state, not institutional memory. No retention guarantees.

Left empty until real departments exist and the Pydantic models in
app/state/ have been used in practice - Phase 11.
"""