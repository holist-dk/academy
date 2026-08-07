# ADR-008: Blackboard Execution Model - Preventing Death Spirals

## Status
Accepted

## Problem
In a Stigmergy/Blackboard architecture, departments communicate only through shared state, not directly. Without explicit constraints, this can produce a "death spiral": departments keep waking each other indefinitely (Reflection updates the learner model, which wakes Curriculum, which wakes Conversation, which produces evidence, which wakes Reflection again...) without the system ever settling on a decision or making meaningful progress.

## Decision
Three architectural laws govern how the Blackboard executes:

Law 1 - Departments communicate only through the Blackboard.
Departments never invoke, schedule, or reference other departments directly, not even indirectly through side effects. A department's only allowed action is to read from and write to the shared state (the ILR / Blackboard).

Law 2 - The Control Shell (LangGraph) is the only scheduler.
It evaluates activation conditions, selects which department runs next, detects convergence, and enforces the maximum iteration limit. No department decides what runs after it.

Law 3 - A Blackboard cycle terminates at a fixed point or at the iteration limit.
A cycle ends when either: (a) no department has anything meaningful left to contribute (a fixed point), or (b) the Control Shell reaches its configured maximum iteration count, at which point it halts and surfaces the state to a human rather than looping silently.

Law 3 extends the retry-limit principle already established in docs/architecture.md (max 3 retries per department) to the whole Blackboard cycle, not just a single department's execution.

Additionally: no department may activate on a background tick or a generic "something changed" signal. Departments only activate in response to new user input or a specific, named condition on the Blackboard (e.g. "new evidence added since my last run," not "the learner model changed"). Once no department has anything left to add, execution stops and waits for the student - the Academy does not keep reasoning indefinitely in the background.

## Supporting Practices (optimizations, not guarantees)
These reduce how often the iteration limit is approached, but do not themselves guarantee termination - only Law 3 does that:
- Activation contracts: departments define a specific, named condition for when they should run, not a vague "state changed" trigger.
- No-op on no contribution: a department that has nothing meaningful to add writes nothing and does not trigger further activation.
- Idempotency: running a department twice on the same Blackboard state produces the same result, or no result. This should fall naturally out of correct activation contracts and no-op behavior, not be implemented as a separate mechanism.
- Provenance: evidence and other Blackboard writes record which department made them and why (already implemented - EvidenceEntry.department, EvidenceEntry.timestamp). This supports debugging a cycle after the fact; it does not prevent loops by itself.

## Alternatives Rejected
- Relying only on activation contracts and no-op behavior to prevent loops, without a hard iteration cap. Rejected - these reduce unnecessary activation but do not mathematically guarantee termination if a contract is misconfigured or a bug causes repeated "meaningful" writes that aren't actually converging.
- Allowing departments to directly trigger other departments for efficiency. Rejected - this breaks Law 1 and reintroduces the coupling Stigmergy is designed to avoid; it also makes the Control Shell no longer the sole source of truth for execution order.

## Consequences
- LangGraph implementation must include a cycle counter with a configured