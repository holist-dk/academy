# ADR-009: Database Persistence Model - Three Layers, Current-State Only for Now

## Status
Accepted

## Problem
The ILR contains information with genuinely different persistence needs: some of it is a permanent historical record (Evidence), some is the Academy's current belief that changes over time (Learner Model, Knowledge Map, Identity, Facts, Metadata), and some is temporary working state for an active lesson (Active Session). Treating all of this as one undifferentiated "save the ILR" operation would force either overly rigid persistence (making everything append-only) or overly loose persistence (losing the append-only guarantee Evidence actually needs). A related question: if Learner Model and Knowledge Map are mutable current-state tables, is the history of how the Academy's beliefs changed over time lost when a value is overwritten?

## Decision
The database is organized into three layers, matching the Information Lifecycle section in docs/architecture.md:

1. Institutional History - EvidenceEntry. One row per entry. Append-only: no UPDATE or DELETE permitted at the database level, not just in Pydantic. This is the permanent record of what was observed.

2. Current Institutional State - LearnerModel, KnowledgeMap, Identity, Facts, Metadata. Mutable tables reflecting the Academy's current belief. Updated in place. For Phase 10, these do NOT retain a history of previous values - only the current state is queryable.

3. Active Session - persisted for crash recovery only (e.g. a mid-lesson server restart should not force the student to restart from nothing), but explicitly treated as cache/infrastructure state, not institutional memory. No retention guarantees. Losing this data is a UX inconvenience, not a loss of anything the Academy "knows" about the student.

## Known, Accepted Gap
Because Layer 2 (Current Institutional State) is current-state-only, the specific historical value of a hypothesis at a past point in time is not reconstructable from the database. Example: if LearnerModel.motivation changes from "high" at 10:00 to "low" at 14:00, only "low" remains queryable afterward. The Evidence Ledger records WHY the belief changed (via supported_by references) but does not itself record WHAT the belief was at each point in time - these are different kinds of historical information, and only the former is preserved by this design.

This gap is accepted deliberately, not overlooked. It is deferred, not rejected.

## Alternatives Considered
- Option A (chosen): current-state only for Layer 2. Simplest, cheapest, matches the project's principle of not modeling complexity before it's needed. No department yet exists to inform what "a meaningful hypothesis change" even looks like in practice.
- Option B (deferred, not rejected): current-state table + a separate history/version table that gains an additional row whenever a hypothesis field meaningfully changes. This would close the gap above without requiring the current-state table to become append-only itself, and without deriving current state by replaying history. This is the option to build if/when the gap above is found to actually matter.
- Option C (rejected for now): full event sourcing, where current state is derived by replaying historical events/evidence rather than being stored directly. Rejected as significantly more architecture than justified today - this is exactly the kind of complexity the project's working principles caution against introducing prematurely ("don't model complexity until the system actually needs it").

## Trigger for Revisiting
Move to Option B when a real, encountered need appears for reconstructing a learner's past hypothesis states - for example, if pedagogical review, auditing, or debugging a department's behavior genuinely requires knowing what the Academy believed at a specific past point in time, not just why it currently believes what it believes.

## Consequences
- EvidenceEntry table must have UPDATE and DELETE revoked at the database permission level (not just enforced by Pydantic's frozen=True, which only protects in-memory objects).
- LearnerModel, KnowledgeMap, Identity, Facts, and Metadata tables are ordinary mutable tables for Phase 10.
- ActiveSession may be persisted for crash recovery but must not be treated as, queried as, or migrated alongside institutional memory.
- If Option B is later adopted, it is additive - it does not require restructuring the current-state tables that Phase 10 establishes.