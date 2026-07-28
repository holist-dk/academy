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

Orchestration is handled by LangGraph, which routes execution between Departments based on task phase. No Department decides what runs next; only the graph does.

See docs/architecture.md and docs/learner_record.md for full detail. Architecture decisions are recorded in docs/adr/.

## Status

### Day 0 - Complete
- Environment: Python 3.14.3, venv, git, GitHub repo (academy, private)
- Full project folder structure scaffolded
- Dependencies installed (FastAPI, LangGraph, LangChain + provider packages, SQLAlchemy, Alembic, Pydantic, psycopg, python-dotenv)
- Documentation written: README.md, docs/charter.md, docs/architecture.md, docs/learner_record.md, docs/departments.md, docs/roadmap.md
- .env.example configured with placeholder keys
- First real code: app/state/evidence.py - EvidenceEntry model (Evidence Ledger), ConfidenceLevel enum, DepartmentName literal - implemented and verified working
- ADR-005: Evidence is append-only
- ADR-006: Department name is a Literal, not an Enum (for now)

### Next Up
- app/state/learner_model.py - EvidenceBackedHypothesis model and LearnerModel (motivation, confidence, curiosity, momentum, frustration, independence)
- Remaining ILR sections: Identity, Facts, Educational History, Knowledge Map, World Engagement, Active Session, Institutional Notes, North Star, Metadata
- LangGraph scaffolding (Phase 9)
- Database scaffolding (Phase 10)
- Department scaffolding (Phase 11)

## Working Principles
- Update this README at the end of every completed work day.
- No file exceeds 300 lines. If one wants to, something foundational needs restructuring.
- Agents have no free will - they execute exactly what is specified.
- Code is 80% deterministic Python, 20% agents (LLM calls).
- When a hurdle is hit: stop, discuss, then continue.
- Long-term project. No rush to ship. Built to last.