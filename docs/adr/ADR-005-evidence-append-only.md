# ADR-005: Evidence Is Append-Only

## Status
Accepted

## Problem
Evidence entries in the Institutional Learner Record represent observations departments make about a learner. If evidence could be edited or deleted after creation, the Academy would lose the ability to explain why it currently believes what it believes, and history could be silently rewritten - intentionally or by bugs.

## Decision
Evidence records are immutable after creation.
- Departments never modify or delete evidence.
- Corrections are represented by new evidence, not by editing old evidence.
- In exceptional technical cases, prior evidence may eventually be marked as superseded rather than deleted. This mechanism is not yet implemented and is deferred until a real need appears (see Consequences).

Implementation: EvidenceEntry (app/state/evidence.py) is a frozen Pydantic model (Config.frozen = True).

## Alternatives Rejected
- Mutable evidence records, editable in place. Rejected because it breaks explainability - the Academy could no longer show why a past conclusion was reached with the evidence available at the time.
- Deleting evidence outright when found to be wrong. Rejected because it destroys the historical record and prevents auditing or replaying a learner's educational journey later.

## Rationale
This mirrors how other institutions and systems treat important records: Git never edits commits, only adds new ones. Accounting systems create correcting transactions rather than altering old ones. Doctors add new diagnoses rather than erasing old ones. The Academy is built to behave like an institution, and this principle is foundational to that.

## Consequences
- Positive: full explainability and auditability; the Academy's understanding changes by accumulating evidence, not rewriting history; enables future features like replaying a learner's journey or testing new learner models against the same historical evidence.
- Deferred work: a "superseded" status and superseded_by reference for evidence found to be produced in error (e.g. a speech recognition bug) is not yet built. Revisit when a department first produces evidence that genuinely needs correcting.
- Deferred work: source reliability (how trustworthy the originating department or source is, distinct from confidence) is not yet modeled. Revisit once the Academy ingests evidence from heterogeneous sources beyond its own departments (self-reports, external assessments, third-party platforms).