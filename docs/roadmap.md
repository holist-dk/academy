# The Academy - Roadmap

## High-Level Sequence
Day 0 (Foundation) -> Sprint 1 -> First Student -> First Lesson -> First Evidence -> First Adaptive Lesson -> RAG -> World Recommendations -> Production

## Day 0 Goal
By the end of Day 0, the only deliverable is a project structure that every future feature naturally fits into. Not working code.

## Day 0 Phases
1. Environment - Python, venv, git, VS Code extensions, GitHub repo.
2. Project Structure - the full folder tree.
3. Dependencies - a minimal, deliberate set. No Redis, Kafka, Celery, or Kubernetes until a real problem requires them.
4. README - written before code. Mission, Purpose, Core Principles, Architecture summary.
5. Architecture Documentation - charter.md, architecture.md, learner_record.md, departments.md, roadmap.md.
6. Configuration - .env.example with placeholder keys only.
7. First Real Code File - institutional_learner_record.py, not main.py. Everything else imports this.
8. Naming Standards - locked terminology, no drift.
9. LangGraph Scaffolding - empty graph/builder.py, nodes.py, routing.py. Architecture before implementation.
10. Database Scaffolding - empty database/models.py, session.py, repository.py. Architecture before connection.
11. Department Scaffolding - five initial departments, identical empty structure each.
12. State Files - state/institutional_learner_record.py, evidence.py, learner_model.py, knowledge_map.py.

## First Week Milestone
Student -> Student Intake Department -> ILR Updated -> Saved -> Returned

If this loop works end to end, it proves: LangGraph works, Departments work, State works, persistence works, and the Blackboard exists. Everything else is additive.

## Working Rule
No new technology unless it solves a problem actually encountered. No Kafka until synchronous communication hurts. No Kubernetes until deployment becomes painful. No Terraform until cloud provisioning becomes repetitive. No Redis until shared ephemeral state is genuinely needed.

## Architecture Decision Records (ADRs)
Every significant decision gets a short written record: the problem, the decision, why it was chosen, alternatives rejected, and consequences. This prevents architecture drift and preserves the reasoning behind decisions as the project grows over months and years.

## Deferred Ideas (not yet decided, not yet built)
Ideas raised in discussion that are plausible but premature - logged here so they are not lost, not because they are scheduled. Revisit only once a real, encountered problem justifies them (per the Working Rule above).

- Discovery / "waggle dance" model: Blackboard entries carrying richer metadata (importance, urgency, confidence, novelty, expected educational impact) instead of bare observations, so departments can prioritize attention rather than react to every write equally. Would require some department to compute these scores - new AI reasoning and schema that don't have a justified use yet with zero departments built.
- Event-driven layer (Kafka, RabbitMQ, NATS, SQS, SNS, EventBridge, or similar) separate from the Blackboard, distinguishing transient "something happened" events from persistent Blackboard state. Matches the project's own Stage 3 roadmap language but is not justified until the current single-Blackboard model has actually been built and has hit a real limitation.

## Status Log
Use this section to track what has actually been completed, updated at the end of each work day per the Founding Charter's working principles.

- 2026-07-27: Day 0 environment, project structure, dependencies, and Phase 5 documentation completed.