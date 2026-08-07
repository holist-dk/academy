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

Orchestration is handled by LangGraph, which routes execution between Departments based on task phase. No Department decides what runs next; only the graph does. Three laws govern this execution model (ADR-008): departments communicate only through the Blackboard, LangGraph is the only scheduler, and every cycle terminates at a fixed point or a hard iteration limit.

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

### Architecture Decision Records
- ADR-005: Evidence is append-only
- ADR-006: Department name is a Literal, not an Enum (for now)
- ADR-007: Student confidence is a separate field from certainty (LearnerModel.student_confidence vs EvidenceBackedHypothesis.certainty)
- ADR-008: Blackboard execution model - the three laws preventing death spirals

### Next Up
- LangGraph scaffolding (Phase 9): graph/builder.py, nodes.py, routing.py - this is where ADR-008's laws (Control Shell as sole scheduler, iteration limit, fixed-point detection) get implemented in code
- Database scaffolding (Phase 10): database/models.py, session.py, repository.py
- Department scaffolding (Phase 11): student_intake, conversation, reflection, curriculum, assessment - each with __init__.py, prompt.md, contract.py, node.py, and an explicit activation contract per ADR-008
- First Week Milestone: Student -> Student Intake Department -> ILR Updated -> Saved -> Returned

## Working Principles
- Update this README at the end of every completed work day.
- No file exceeds 300 lines. If one wants to, something foundational needs restructuring.
- Agents have no free will - they execute exactly what is specified.
- Code is 80% deterministic Python, 20% agents (LLM calls).
- When a hurdle is hit: stop, discuss, then continue.
- Long-term project. No rush to ship. Built to last.