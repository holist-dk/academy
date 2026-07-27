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

See docs/architecture.md and docs/learner_record.md for full detail.