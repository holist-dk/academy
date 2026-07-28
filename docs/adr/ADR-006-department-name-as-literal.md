# ADR-006: Department Name Is a Literal, Not an Enum

## Status
Accepted

## Problem
Evidence entries must record which department produced them. A bare string field (department: str) allows typos and inconsistent values ("Conversation", "conversation", "Conv") to enter the record permanently, which is especially costly given evidence is append-only (ADR-005). But the Academy's organizational structure - the actual set of departments - is still being discovered. It has already been renamed and restructured multiple times (Agents -> Departments; uncertainty over whether Conversation is one department or several; whether World Engagement is a department or a capability).

## Decision
Department names are typed as a Literal of currently known department strings (DepartmentName in app/state/evidence.py), not a str and not an Enum.

    DepartmentName = Literal[
        "student_intake",
        "conversation",
        "reflection",
        "curriculum",
        "assessment",
    ]

Adding a new department means adding one string to this Literal.

## Alternatives Rejected
- Plain str. Rejected because it permits typos and inconsistent values with no validation, and evidence is immutable once created - a typo would live in the record forever.
- Enum (class Department(Enum): ...). Not rejected outright, but deferred. An enum communicates "these are the canonical departments," which overstates how settled the organizational structure currently is. Locking an enum today risks freezing a taxonomy that is still being actively discovered.
- DepartmentRegistry (dynamic plugin-style department registration). Rejected for now as premature complexity - this solves a scaling problem (departments as independently loadable plugins) the Academy does not have yet.

## Rationale
A Literal gives the same typo protection as an enum - Pydantic rejects any value not in the list - while being a one-line edit to extend, and without implying the department list is finalized. This matches the project's working principle: don't introduce complexity (or premature permanence) until it solves a real, current problem.

## Consequences
- Positive: typos are caught by Pydantic validation; adding a department during ongoing org-structure discovery is cheap.
- Migration path: once the department/org structure stabilizes (target: after Sprint 1, once real departments are built and their boundaries are proven in practice), migrate DepartmentName to a proper Department(str, Enum). If departments later become dynamically loaded plugins, consider a DepartmentRegistry instead.
- This decision should be revisited, not treated as permanent - unlike ADR-005, which is intended to hold indefinitely.