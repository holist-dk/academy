# The Academy

## Mission
Protect the student's curiosity.

## Purpose
Build an educational institution - not a chatbot - that helps learners become independent Japanese language learners.

## Core Principles
- Evidence over assumptions
- Understanding over memorization
- Real-world application
- Recommend the world - the Academy points learners to real Japanese-speaking resources and communities rather than trying to contain them inside the app

## Architecture
The Academy is built on a Blackboard Architecture: specialist Departments (agents) never call each other directly. They communicate indirectly by reading and writing to a shared record - the Institutional Learner Record (ILR) - the canonical, evidence-backed understanding of each learner.

Orchestration is handled by LangGraph, which routes execution between Departments based on task phase. No Department decides what runs next; only the graph does. Four laws govern this execution model (ADR-008): departments communicate only through the Blackboard, LangGraph is the only scheduler, every cycle terminates at a fixed point or a hard iteration limit, and Blackboard entries describe reality, never intent (no entry may suggest which department should act on it).

Information is organized into three lifecycle tiers (see docs/architecture.md, "Information Lifecycle"): events (deferred), Blackboard/Active Session state (temporary), and institutional memory (durable - Evidence Ledger, Learner Model, Knowledge Map, etc.). The database (ADR-009) follows the same three-layer split: append-only Evidence, mutable current-state tables for everything else, and a crash-recovery-only cache for Active Session.

See docs/architecture.md and docs/learner_record.md for full detail. Architecture decisions are recorded in docs/adr/.

## Status

### Day 0 - Complete
- Environment: Python 3.14.3, venv, git, GitHub repo (holist-dk/academy, private)
- Full project folder structure scaffolded
- Dependencies installed (FastAPI, LangGraph, LangChain + provider packages, SQLAlchemy, Alembic, Pydantic, psycopg, python-dotenv)
- Documentation written: README.md, docs/charter.md, docs/architecture.md, docs/learner_record.md, docs/departments.md, docs/roadmap.md
- .env.example configured with placeholder keys

### ILR Implementation - Complete (Phase 12)
- app/state/evidence.py - EvidenceEntry model, ConfidenceLevel enum, DepartmentName literal. Implemented and verified.
- app/state/learner_model.py - EvidenceBackedHypothesis model (with unknown-state defaults), LearnerModel (motivation, student_confidence, curiosity, momentum, frustration, independence), LearnerModel.new_unknown() convenience constructor, EvidenceId alias. Implemented and verified.
- app/state/knowledge_map.py - MasteryLevel enum, KnowledgeConcept model, KnowledgeSubject, KnowledgeMap (grammar, vocabulary, kanji, listening, speaking, reading, writing, culture). Implemented and verified.
- app/state/institutional_learner_record.py - root ILR object composing all of the above: Identity, Facts, Evidence Ledger, Learner Model, Educational History, Knowledge Map, World Engagement, Active Session, Institutional Notes, North Star, Metadata. Implemented and verified end to end.

### LangGraph Scaffolding - Complete (Phase 9)
- app/graph/builder.py, nodes.py, routing.py - documented empty scaffolding, ready for Phase 11 departments to be wired in.
- scripts/langgraph_toy/toy_graph.py - working reference example demonstrating the Control Shell pattern (state flow through nodes, iteration limit stopping a death spiral). Kept as a learning/reference artifact, not part of the real system.

### Database Scaffolding - Complete (Phase 10)
- app/database/models.py, session.py, repository.py - documented empty scaffolding, per ADR-009's three-layer persistence model (append-only Evidence, mutable current-state tables, cache-only Active Session).
- Repository layer designed to be the only code allowed to touch the database directly - departments will call repository functions, never issue raw queries.

### Architecture Decision Records
- ADR-005: Evidence is append-only
- ADR-006: Department name is a Literal, not an Enum (for now)
- ADR-007: Student confidence is a separate field from certainty (LearnerModel.student_confidence vs EvidenceBackedHypothesis.certainty)
- ADR-008: Blackboard execution model - the four laws preventing death spirals (Law 4: Blackboard entries describe reality, never intent)
- ADR-009: Database persistence model - three layers (append-only Evidence, mutable current-state, cache-only Active Session). Documents a known, accepted gap: historical hypothesis states are not reconstructable until/unless Option B (a separate history/version table) is built.

### Deferred Ideas (see docs/roadmap.md for detail)
- Discovery/"waggle dance" model - richer Blackboard entries with importance/urgency/confidence scoring
- Event-driven layer (Kafka/RabbitMQ/NATS/etc.) separate from the Blackboard
- LearnerModel/KnowledgeMap history/versioning (ADR-009 Option B) - revisit if reconstructing past hypothesis states becomes a real, encountered need
All logged, not scheduled - revisit only once a real encountered problem justifies them.

### Next Up: Phase 11 - Department Scaffolding
- Create the five initial department folders: student_intake, conversation, reflection, curriculum, assessment
- Each gets the standard structure: __init__.py, prompt.md, contract.py, node.py
- contract.py must define an explicit activation contract per ADR-008 (a specific, named condition for when the department runs - not a vague "state changed" trigger)
- prompt.md written as constraints, not descriptions (per the Prompt Engineering as Constraint-Writing principle in docs/architecture.md)
- This is the last structural phase before real department behavior gets implemented and wired into the LangGraph scaffolding from Phase 9
- First Week Milestone (the actual proof of all of this working together): Student -> Student Intake Department -> ILR Updated -> Saved -> Returned

## Working Principles
- Update this README at the end of every completed work day.
- No file exceeds 300 lines. If one wants to, something foundational needs restructuring.
- Agents have no free will - they execute exactly what is specified.
- Code is 80% deterministic Python, 20% agents (LLM calls).
- When a hurdle is hit: stop, discuss, then continue.
- Long-term project. No rush to ship. Built to last.