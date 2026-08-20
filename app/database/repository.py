"""
Repository layer - the only code allowed to talk to the database directly.

Departments never issue raw queries. They call repository functions
(e.g. add_evidence(), get_current_learner_model()), which enforce the
three-layer rules from ADR-009 - in particular, that EvidenceEntry
writes are append-only (insert only, no update/delete path exposed
here at all).

Left empty until Phase 11 (departments) need real read/write operations.
"""